from http.client import HTTPException

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.auth import verify_password, get_password_hash, create_access_token, decode_access_token
from src.exts import get_db
from src.form.userform import UserForm
from src.logging.logger import debug, warn, error
from src.model.user import UserModel

router = APIRouter(
    prefix="/user",
    tags=["user"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@router.post("/register", status_code=status.HTTP_200_OK)
async def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    found_user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if found_user:
        return {
            "msg": "user exist"
        }, status.HTTP_400_BAD_REQUEST

    user = UserModel(username=form_data.username, password_hashed=get_password_hash(form_data.password))
    db.add(user)
    db.commit()
    debug(f"{form_data.username}注册成功")
    return {
        "msg": "success"
    }


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    found_user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not found_user:
        return {
            "msg": "not found user"
        }, status.HTTP_400_BAD_REQUEST
    if verify_password(form_data.password, found_user.password_hashed):
        access_token = create_access_token(data={"username": form_data.username})
        debug("登录成功")
        return {
            "access_token": access_token,
            "msg": "success",
        }
    return {
        "msg": "fail"
    }, status.HTTP_400_BAD_REQUEST


@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    debug(f"正在查找用户id: {user_id}")
    found_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not found_user:
        warn(f"没有找到id({user_id})的用户")
        return {
            "msg": "not found"
        }, 403
    debug(f"已找到id({user_id})的用户")
    return found_user, 200


@router.put("/", status_code=HTTP_201_CREATED)
async def update_user(user: UserForm, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
    except HTTPException as e:
        error(f"解码jwt错误: {e}")
        return {
            "msg": "jwt error"
        }, status.HTTP_400_BAD_REQUEST

    current_username = payload.get("username")
    if not current_username:
        error("jwt没有username信息")

    found_user = db.query(UserModel).filter(UserModel.username == current_username).first()
    if not found_user:
        warn(f"未查找到用户: {current_username}")
        return {
            "msg": "not found"
        }, status.HTTP_404_NOT_FOUND

    if user.username:
        found_user.username = user.username
    if user.password:
        found_user.password_hashed = get_password_hash(user.password)
    if user.desc:
        found_user.desc = user.desc
    db.add(found_user)
    db.commit()
    debug(f"成功更新用户: {current_username}")
    return {
        "id": found_user.id,
        "username": found_user.username,
        "desc": found_user.desc,
        "msg": "success",
    }


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
    except HTTPException as e:
        error(f"解码jwt错误: {e}")
        return {
            "msg": "jwt error"
        }, status.HTTP_400_BAD_REQUEST

    current_username = payload.get("username")
    if not current_username:
        error(f"jwt没有username信息: {current_username}")
        return {
            "msg": "jwt error"
        }, status.HTTP_400_BAD_REQUEST
    user = db.query(UserModel).filter(UserModel.username == current_username).first()
    if user:
        db.delete(user)
        db.commit()
        debug(f"成功删除用户: {current_username}")
        return {
            "msg": "success",
        }, status.HTTP_200_OK
    return {
        "msg": "not found user"
    }, status.HTTP_404_NOT_FOUND
