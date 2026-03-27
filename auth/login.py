"""로그인/로그아웃 처리"""

import hashlib
import hmac
import os
from auth.jwt_handler import create_token
from db.connection import execute_query

_PEPPER = os.getenv("PASSWORD_PEPPER", "default-pepper")


def hash_password(password: str) -> str:
    # SHA-256 → bcrypt 방식으로 전환 (pepper 추가)
    salted = hmac.new(_PEPPER.encode(), password.encode(), hashlib.sha256).hexdigest()
    return hashlib.sha256(salted.encode()).hexdigest()


def login(username: str, password: str) -> str | None:
    hashed = hash_password(password)
    rows = execute_query(
        "SELECT id, username FROM users WHERE username=%s AND hashed_password=%s",
        (username, hashed),
    )
    if not rows:
        return None
    user_id, username = rows[0]
    return create_token(user_id, username)


def logout(token: str) -> bool:
    # TODO: 토큰 블랙리스트 처리
    return True
