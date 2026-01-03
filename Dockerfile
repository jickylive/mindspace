# 1. 使用轻量级基础镜像
FROM python:3.9-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 先复制依赖文件并安装（利用 Docker 缓存层）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 复制项目代码
COPY . .

# 5. 确保数据目录存在
RUN mkdir -p /app/data

# 6. 容器启动时：先执行同步脚本入库，再启动 Web 服务
# 使用 gunicorn 提升在高并发下的稳定性
CMD python sync_content.py && gunicorn -w 4 -b 0.0.0.0:5000 app:app