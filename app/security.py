"""密码哈希 + JWT 令牌：认证体系的两块基石"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

# ⚠️ 开发用的密钥。生产环境必须放进环境变量（.env），绝不能写死在代码里提交！
SECRET_KEY = "dev-secret-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 令牌有效期 1 天


def hash_password(password: str) -> str:
    """把明文密码变成哈希值（不可逆，无法还原出原密码）

    bcrypt 会自动生成随机的“盐”，同一密码每次哈希结果都不同。
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """校验明文密码和数据库里的哈希值是否匹配"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(user_id: int) -> str:
    """签发一个 JWT

    JWT 是三段式：header.payload.signature
    payload 里放“这是谁(sub)”和“什么时候过期(exp)”，用密钥签名防篡改。
    """
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int | None:
    """校验 JWT 并取出 user_id；令牌无效或过期则返回 None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        return None
