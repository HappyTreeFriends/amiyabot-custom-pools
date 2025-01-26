import random
import shutil
import uuid
from cachetools import TTLCache
from fastapi import FastAPI, HTTPException, File, UploadFile, Request, APIRouter,Query,Depends
from typing import Optional
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import json
import os
import uvicorn
from contextlib import contextmanager
import zipfile
import io
from fastapi.staticfiles import StaticFiles

# 创建 FastAPI 实例
app = FastAPI()
router = APIRouter()

TEMP_DIR = "./data/temp"
UPLOAD_DIR = "./data/uploads"

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

SQLITE_DB = "./data/db.sqlite3"

app.mount("/pools", StaticFiles(directory=UPLOAD_DIR), name="pools")

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

@contextmanager
def get_db():
    # 创建 SQLite 连接
    conn = sqlite3.connect("./data/db.sqlite3")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# 根接口
@app.get("/")
def read_root():
    return {"message": "Welcome to the server!"}

search_cache = TTLCache(maxsize=1000, ttl=60)

def search_rate_limiter(request: Request):
    """搜索操作频率限制（仅当有搜索参数时生效）"""
    if request.query_params.get("search"):
        client_ip = request.client.host
        if client_ip in search_cache:
            raise HTTPException(
                status_code=429,
                detail="Search operations are limited to 1 request per minute."
            )
        search_cache[client_ip] = True
    return

@app.on_event("startup")
async def startup():
    # 使用 SQLite 创建表
    conn = sqlite3.connect("./data/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS custom_pools (
        pool_uuid TEXT PRIMARY KEY,
        unique_name TEXT,
        edit_uuid TEXT,
        file_name TEXT,
        operators TEXT,
        use_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

@app.post("/upload-zip")
async def upload_json(file: UploadFile = File(...), pool_uuid: str = None, edit_uuid: str = None):
    # 检查文件大小
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 50MB limit.")
    
    # 检查文件类型
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="File is not a ZIP file.")
    
    # 临时写入数据库并获取该数据库对象
    with get_db() as conn:
        if not pool_uuid:
            # 生成 pool_uuid
            pool_uuid = str(uuid.uuid4())
            edit_uuid = str(uuid.uuid4())

            cursor = conn.cursor()
            cursor.execute("INSERT INTO custom_pools (pool_uuid, edit_uuid) VALUES (?, ?)", (pool_uuid, edit_uuid))
            conn.commit()

        # 检查 pool_uuid 是否存在
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM custom_pools WHERE pool_uuid = ?", (pool_uuid,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="pool_uuid not found.")
        if row["edit_uuid"] != edit_uuid:
            raise HTTPException(status_code=400, detail="edit_uuid does not match.")

    # unzip this file in memory
    with zipfile.ZipFile(io.BytesIO(await file.read()), "r") as zip_ref:
        zip_ref.extractall(os.path.join(TEMP_DIR, pool_uuid))

    pool_temp_dir = os.path.join(TEMP_DIR, pool_uuid)

    # 打开meta-data.json文件

    with open(os.path.join(pool_temp_dir, "meta-data.json"), "r") as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format.")
    
    # 检查json数据
    if not isinstance(json_data, dict):
        raise HTTPException(status_code=400, detail="JSON data must be a dictionary.")
    
    # 覆写pool_uuid
    json_data["pool_uuid"] = pool_uuid

    if "pool_name" not in json_data:
        raise HTTPException(status_code=400, detail="pool_name is required.")

    if row["unique_name"] is None:
        for _ in range(50):
            unique_name = json_data.get("pool_name") + "#" + str(random.randint(1000, 9999))
            cursor.execute("SELECT * FROM custom_pools WHERE unique_name = ?", (unique_name,))
            peekRow = cursor.fetchone()
            if not peekRow:
                break
        else:
            raise HTTPException(status_code=500, detail="Failed to generate unique_name.")
        
        cursor.execute("UPDATE custom_pools SET unique_name = ? WHERE pool_uuid = ?", (unique_name, pool_uuid))

        json_data["unique_name"] = unique_name
    
    # 检查images文件夹是否存在
    pool_dir = os.path.join(UPLOAD_DIR, pool_uuid)
    os.makedirs(pool_dir, exist_ok=True)

    # 移动文件pool_image.png
    os.rename(os.path.join(pool_temp_dir, "pool_image.png"), os.path.join(pool_dir, "pool_image.png"))

    if 'custom_operators' in json_data:
        for operator in json_data['custom_operators']:
            avatar_file = os.path.join(pool_temp_dir, operator['uuid']+".avatar.png")
            portrait_file = os.path.join(pool_temp_dir, operator['uuid']+".portrait.png")
            if os.path.exists(avatar_file):
                os.rename(avatar_file, os.path.join(pool_dir, operator['uuid']+".avatar.png"))
            if os.path.exists(portrait_file):
                os.rename(portrait_file, os.path.join(pool_dir, operator['uuid']+".portrait.png"))
    
    # json_data重整(只保留指定的key)
    # refined_json_data = {key: json_data[key] for key in ["pool_uuid", "pool_name", "unique_name", "custom_operators"]}
    refined_json_data = json_data

    # 写入json文件
    json_path = os.path.join(pool_dir, "meta-data.json")
    with open(json_path, "w") as f:
        json.dump(refined_json_data, f, indent=4)

    # 写入数据库
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE custom_pools SET file_name = ? WHERE pool_uuid = ?", (json_path, pool_uuid))
        conn.commit()

    # 清理临时文件夹
    shutil.rmtree(pool_temp_dir)
    
    return {"message": "File uploaded successfully.", "unique_name": unique_name, "edit_uuid": edit_uuid}

@app.post("/get-pool-uuid/")
async def get_pool_uuid(request: dict):
    # 从请求体中获取 unique_name
    unique_name = request.get("unique_name")
    
    if not unique_name:
        raise HTTPException(status_code=400, detail="unique_name is required.")
    
    if not isinstance(unique_name, str):
        raise HTTPException(status_code=400, detail="unique_name must be a string.")
    
    # 查询数据库，查找对应的 pool_uuid
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT pool_uuid FROM custom_pools WHERE unique_name = ?", (unique_name,))
        row = cursor.fetchone()

        if row:
            return {"pool_uuid": row["pool_uuid"]}
        else:
            raise HTTPException(status_code=404, detail="unique_name not found.")

@app.post("/increment-use-count/")
async def increment_use_count(request: dict):
    # 获取 pool_uuid
    pool_uuid = request.get("pool_uuid")
    
    if not pool_uuid:
        raise HTTPException(status_code=400, detail="pool_uuid is required.")
    
    if not isinstance(pool_uuid, str):
        raise HTTPException(status_code=400, detail="pool_uuid must be a string.")
    
    # 更新 use_count
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT use_count FROM custom_pools WHERE pool_uuid = ?", (pool_uuid,))
        row = cursor.fetchone()

        if row:
            # use_count 存在，执行更新
            cursor.execute("UPDATE custom_pools SET use_count = use_count + 1 WHERE pool_uuid = ?", (pool_uuid,))
            conn.commit()
            return {"message": f"use_count for pool_uuid {pool_uuid} incremented by 1."}
        else:
            # pool_uuid 不存在
            raise HTTPException(status_code=404, detail="pool_uuid not found.")

@app.get("/top-use-count-pools/")
async def top_use_count_pools():
    # 查询数据库，按照 use_count 降序排列，获取前十个 pool_uuid
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pool_uuid FROM custom_pools
            ORDER BY use_count DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()

        # 提取 pool_uuid 列表
        pool_uuids = [row["pool_uuid"] for row in rows]

        return {"top_use_count_pools": pool_uuids}

@router.get("/pools", dependencies=[Depends(search_rate_limiter)])
async def list_pools(
    request: Request,
    search: Optional[str] = Query(None, min_length=1, description="Search in unique_name or operators"),
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    size: int = Query(10, ge=1, le=100, description="Items per page (1-100)"),
    db: sqlite3.Connection = Depends(get_db)
):
    # 计算分页偏移量
    offset = (page - 1) * size
    
    # 构建基础查询
    base_query = "SELECT * FROM custom_pools"
    count_query = "SELECT COUNT(*) FROM custom_pools"
    params = []
    
    # 添加搜索条件
    if search:
        search_term = f"%{search}%"
        where_clause = " WHERE unique_name LIKE ? OR operators LIKE ?"
        base_query += where_clause
        count_query += where_clause
        params.extend([search_term, search_term])
    
    # 添加排序和分页
    base_query += " ORDER BY use_count DESC LIMIT ? OFFSET ?"
    
    try:
        # 执行分页查询
        cursor = db.execute(base_query, params + [size, offset])
        filtered_pools = []
        for pool in cursor.fetchall():
            filtered_pools.append({
                "uuid": pool["pool_uuid"],  # 根据表结构使用正确字段名
                "unique_name": pool["unique_name"],
                "operators": pool["operators"]
            })
        
        # 执行总数查询
        cursor = db.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        return {
            "data": filtered_pools,
            "pagination": {
                "total": total,
                "page": page,
                "size": size,
                "total_pages": (total + size - 1) // size
            }
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)