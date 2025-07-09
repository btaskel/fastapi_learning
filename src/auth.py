from datetime import timezone, datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.config import SECRET_KEY
from src.model.user import UserModel

# 使用的算法是Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# 校验密码：校验接收的密码是否匹配存储的哈希值。
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token 无效")

if __name__ == '__main__':
    hashed_pw = get_password_hash("1246")
    print(hashed_pw)
    print(verify_password("1246", hashed_pw))