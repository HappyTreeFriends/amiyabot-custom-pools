import random
import uuid
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import json
import os
import uvicorn
from contextlib import contextmanager

# 创建 FastAPI 实例
app = FastAPI()

SQLITE_DB = "./data/db.sqlite3"

UPLOAD_DIR = "./data/uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    return {"message": "Welcome to the FastAPI server!"}

@app.on_event("startup")
async def startup():
    # 使用 SQLite 创建表
    conn = sqlite3.connect("./data/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS custom_pools (
        pool_uuid TEXT PRIMARY KEY,
        unique_name TEXT,
        file_name TEXT,
        edit_uuid TEXT,
        use_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

@app.post("/upload-json/")
async def upload_json(file: UploadFile = File(...)):
    # 检查文件大小
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 50MB limit.")
    
    # 检查文件类型
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="File is not a JSON file.")
    
    # 读取文件内容
    file_content = await file.read()

    # 验证文件内容是否为有效的 JSON
    try:
        json_data = json.loads(file_content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
    
    pool_uuid = json_data.get("pool_uuid")

    if not pool_uuid:
        raise HTTPException(status_code=400, detail="pool_uuid is required.")
    
    if not isinstance(pool_uuid, str):
        raise HTTPException(status_code=400, detail="pool_uuid must be a string.")


    file_name = "Custom-"+pool_uuid+".json"

    # 检查数据库是否存在
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM custom_pools WHERE pool_uuid = ?", (pool_uuid,))
        row = cursor.fetchone()
        if row:
            # exist in database, 比较 edit_uuid
            edit_uuid = json_data.get("edit_uuid")
            if not edit_uuid:
                raise HTTPException(status_code=400, detail="edit_uuid is required for existing pool.")
            if not isinstance(edit_uuid, str):
                raise HTTPException(status_code=400, detail="edit_uuid must be a string.")
            if row["edit_uuid"] != edit_uuid:
                raise HTTPException(status_code=400, detail="edit_uuid does not match.")
            
            unique_name = row["unique_name"]
            edit_uuid = None
        else:
            # not exist in database, 添加到数据库
            # generate an edit_uuid
            edit_uuid = str(uuid.uuid4()).replace('-', '')
            
            # 生成unique_name
            # json中获取的pool_name#XXXX 4位随机数
            # 和数据库中不重复即可
            # 最多循环10次，如果还是找不到，就返回错误

            for _ in range(10):
                unique_name = json_data.get("pool_name") + "#" + str(random.randint(1000, 9999))
                cursor.execute("SELECT * FROM custom_pools WHERE unique_name = ?", (unique_name,))
                row = cursor.fetchone()
                if not row:
                    break
            else:
                raise HTTPException(status_code=500, detail="Failed to generate unique_name.")

            cursor.execute("INSERT INTO custom_pools (pool_uuid, unique_name, file_name, edit_uuid) VALUES (?, ?, ?, ?)", (pool_uuid, unique_name, file_name , edit_uuid))
            conn.commit()
    
    # 保存文件到指定目录
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(file_content)
    
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

@app.get("/download-json/{pool_uuid}")
async def download_json(pool_uuid: str):
    # 查询数据库，查找对应的 file_name
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT file_name FROM custom_pools WHERE pool_uuid = ?", (pool_uuid,))
        row = cursor.fetchone()

        if row:
            # 构造文件路径
            file_name = row["file_name"]
            file_path = os.path.join(UPLOAD_DIR, file_name)

            if os.path.exists(file_path):
                # 返回文件内容作为响应
                return FileResponse(file_path, media_type="application/json", filename=file_name)
            else:
                raise HTTPException(status_code=404, detail="File not found.")
        else:
            raise HTTPException(status_code=404, detail="pool_uuid not found.")

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)