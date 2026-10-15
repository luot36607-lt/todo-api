from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import User, UserCreate, UserRead
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    """注册：用户名必须唯一，密码只存哈希"""
    existing = session.exec(
        select(User).where(User.username == user_in.username)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已被占用")

    user = User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login")
def login(user_in: UserCreate, session: Session = Depends(get_session)):
    """登录：校验密码，成功则签发 JWT"""
    user = session.exec(
        select(User).where(User.username == user_in.username)
    ).first()

    # 提示故意写得一样：不泄露“这个用户名是否存在”
    if user is None or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
