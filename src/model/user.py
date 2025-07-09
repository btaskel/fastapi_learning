from sqlalchemy import Column, Integer, String

from src.exts import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user_table"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hashed = Column(String(128), nullable=False)  # 使用sha256存储
    desc = Column(String(256), nullable=True, index=True)

if __name__ == '__main__':
    user = UserModel(username="bt", password_hashed="wadawd", desc="eeee")
    print(vars(user))