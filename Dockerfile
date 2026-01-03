# 1. 使用多架构支持良好的官方轻量镜像
FROM python:3.9-slim AS builder

# 尝试使用南京大学或上海交大的代理地址
# FROM docker.nju.edu.cn/library/python:3.9-slim

# 或者使用 DaoCloud 镜像
# FROM docker.m.daocloud.io/library/python:3.9-slim AS builder

# 2. 设置环境变量
# 防止 Python 产生 .pyc 编译文件
ENV PYTHONDONTWRITEBYTECODE=1
# 强制 stdout 和 stderr 实时流向控制台，方便 Docker 查看日志
ENV PYTHONUNBUFFERED=1
# 设置数据库存储路径
ENV DATABASE_PATH=/app/data/mindspace.db

# 3. 设置工作目录
WORKDIR /app

# 4. 安装系统基础工具（可选，如需在容器内进行简单调试）
# 对于多架构构建，避免安装特定架构的二进制库，尽量依赖 pip 编译
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
 
# 5. 复制依赖清单并安装
# 利用 Docker 缓存机制，只有 requirements.txt 变化时才重新安装
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. 复制项目代码
COPY --from=builder /root/.local /root/.local
COPY . .

# 7. 预创建数据目录并设置权限
# 确保在任何用户模式下都有权限写入数据库
RUN mkdir -p /app/data && chmod 777 /app/data

# 8. 暴露端口 (根据你的 app.py 端口设置)
EXPOSE 5001

# 9. 启动流程：先同步/初始化数据，再运行生产级服务器 Gunicorn
# -w 4: 启动 4 个进程处理请求
# -b 0.0.0.0: 绑定所有网络接口
CMD ["sh", "-c", "python sync_content.py && gunicorn -w 4 -b 0.0.0.0:5001 app:app"]