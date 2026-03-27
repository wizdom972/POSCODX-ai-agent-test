"""JWT 토큰 발급 및 검증"""

import jwt
from datetime import datetime, timedelta
from config.settings import JWT, SECRET_KEY

REFRESH_SECRET_KEY = SECRET_KEY + "-refresh"


def create_token(user_id: int, username: str) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=JWT["expire_minutes"]),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT["algorithm"])


def create_refresh_token(user_id: int) -> str:
    """리프레시 토큰을 발급합니다. 액세스 토큰 만료 시 재발급에 사용합니다."""
    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=JWT["refresh_expire_days"]),
    }
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=JWT["algorithm"])


def verify_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[JWT["algorithm"]])


def verify_refresh_token(token: str) -> dict:
    """리프레시 토큰을 검증하고 페이로드를 반환합니다."""
    payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[JWT["algorithm"]])
    if payload.get("type") != "refresh":
        raise jwt.InvalidTokenError("리프레시 토큰이 아닙니다.")
    return payload


def refresh_access_token(refresh_token: str) -> str:
    """리프레시 토큰으로 새 액세스 토큰을 발급합니다."""
    payload = verify_refresh_token(refresh_token)
    return create_token(user_id=payload["sub"], username=payload.get("username", ""))
