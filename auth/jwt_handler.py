"""JWT 토큰 발급 및 검증"""

import jwt
from datetime import datetime, timedelta
from config.settings import JWT, SECRET_KEY


def create_token(user_id: int, username: str) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=JWT["expire_minutes"]),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT["algorithm"])


def verify_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[JWT["algorithm"]])
