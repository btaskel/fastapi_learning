FROM python:3.11.9

# ---配置测试环境---
# 切换目录，在容器内部的root下创建个app
WORKDIR /app

# 暴露端口
EXPOSE 4000

# copy src dst
COPY requirements.txt .

# --no-cache-dir关闭pip http缓存
RUN pip install --no-cache-dir -r requirements.txt

# copy any to any
COPY . .

# ---!RUN!---

# 进行数据库迁移
CMD ["alembic", "init", "alembic"]
# autogenerate 自动sql生成
CMD ["alembic", "revision", "--autogenerate","-m","\"init\""]
# head 假设有多个迁移脚本未执行，则逐步执行到最新迁移脚本
CMD ["alembic", "upgrade", "head"]

# 启动api
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "4000"]