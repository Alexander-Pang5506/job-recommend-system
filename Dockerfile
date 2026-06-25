# 使用 Python 3.13
FROM python:3.13-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput || true

# Render 会自动设置 PORT 环境变量
EXPOSE 8000

# 启动命令：先迁移数据库，再启动 gunicorn
CMD ["sh", "-c", "python manage.py migrate --run-syncdb && gunicorn JobRecommend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120"]
