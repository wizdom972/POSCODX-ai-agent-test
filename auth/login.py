"""로그인/로그아웃 처리"""

import hashlib
import hmac
import os
from collections import defaultdict
from datetime import datetime, timedelta

from auth.jwt_handler import create_token
from db.connection import execute_query

_PEPPER = os.getenv("PASSWORD_PEPPER", "default-pepper")

# 로그인 실패 횟수 추적 (IP → [실패 시각 목록])
_login_attempts: dict[str, list[datetime]] = defaultdict(list)
MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


def _is_locked(ip: str) -> bool:
    """IP가 잠금 상태인지 확인합니다."""
    cutoff = datetime.now() - timedelta(minutes=LOCKOUT_MINUTES)
    _login_attempts[ip] = [t for t in _login_attempts[ip] if t > cutoff]
    return len(_login_attempts[ip]) >= MAX_ATTEMPTS


def _record_failure(ip: str):
    _login_attempts[ip].append(datetime.now())


def hash_password(password: str) -> str:
    salted = hmac.new(_PEPPER.encode(), password.encode(), hashlib.sha256).hexdigest()
    return hashlib.sha256(salted.encode()).hexdigest()


def login(username: str, password: str, ip: str = "0.0.0.0") -> str | None:
    if _is_locked(ip):
        raise PermissionError(f"로그인 시도가 너무 많습니다. {LOCKOUT_MINUTES}분 후 다시 시도하세요.")

    hashed = hash_password(password)
    rows = execute_query(
        "SELECT id, username FROM users WHERE username=%s AND hashed_password=%s",
        (username, hashed),
    )
    if not rows:
        _record_failure(ip)
        return None

    # 성공 시 실패 기록 초기화
    _login_attempts[ip] = []
    user_id, username = rows[0]
    return create_token(user_id, username)


def logout(token: str) -> bool:
    # TODO: 토큰 블랙리스트 처리
    return True
