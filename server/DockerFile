# 使用官方 Python 3.11 镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的所有文件到容器中的工作目录
COPY . /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用端口
EXPOSE 30080

# 启动 FastAPI 应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
