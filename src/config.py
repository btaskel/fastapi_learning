import os
import pathlib

# ROOT
ROOT_PATH: pathlib.Path = pathlib.Path.cwd()

# DATA
DATA_PATH: pathlib.Path = ROOT_PATH / "data"

# 初始化DB配置
# SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:root@127.0.0.1:3306/fastapi_test"
SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")

LOGGER_LEVEL: str = "debug"
DEBUG_FILE_PATH: pathlib.Path = DATA_PATH / "debug.log"

# JWT
# SECRET_KEY = "4da4c59f-0618-4d1a-9c16-f000ba823b60"
SECRET_KEY = os.getenv("SECRET_KEY")

if __name__ == '__main__':
    print(DEBUG_FILE_PATH)