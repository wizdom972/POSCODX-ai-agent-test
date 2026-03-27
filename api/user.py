"""사용자 API 엔드포인트"""

import re

from auth.login import login
from db.connection import execute_query

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$")


def _validate_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email))


def _validate_password(password: str) -> list[str]:
    errors = []
    if len(password) < 8:
        errors.append("비밀번호는 8자 이상이어야 합니다.")
    if not re.search(r"[A-Z]", password):
        errors.append("대문자를 1자 이상 포함해야 합니다.")
    if not re.search(r"\d", password):
        errors.append("숫자를 1자 이상 포함해야 합니다.")
    return errors


def get_user(user_id: int) -> dict | None:
    rows = execute_query("SELECT id, username, email FROM users WHERE id=%s", (user_id,))
    if not rows:
        return None
    id_, username, email = rows[0]
    return {"id": id_, "username": username, "email": email}


def create_user(username: str, email: str, password: str) -> dict:
    if not _validate_email(email):
        return {"error": "유효하지 않은 이메일 형식입니다."}

    pw_errors = _validate_password(password)
    if pw_errors:
        return {"error": pw_errors}

    from auth.login import hash_password
    hashed = hash_password(password)
    execute_query(
        "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)",
        (username, email, hashed),
    )
    return {"username": username, "email": email}


def login_user(username: str, password: str, ip: str = "0.0.0.0") -> dict:
    try:
        token = login(username, password, ip=ip)
    except PermissionError as e:
        return {"error": str(e)}
    if not token:
        return {"error": "인증 실패"}
    return {"token": token}
