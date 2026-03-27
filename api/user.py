"""사용자 API 엔드포인트"""

from auth.login import login
from db.connection import execute_query


def get_user(user_id: int) -> dict | None:
    rows = execute_query("SELECT id, username, email FROM users WHERE id=%s", (user_id,))
    if not rows:
        return None
    id_, username, email = rows[0]
    return {"id": id_, "username": username, "email": email}


def create_user(username: str, email: str, password: str) -> dict:
    from auth.login import hash_password
    hashed = hash_password(password)
    execute_query(
        "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)",
        (username, email, hashed),
    )
    return {"username": username, "email": email}


def login_user(username: str, password: str) -> dict:
    token = login(username, password)
    if not token:
        return {"error": "인증 실패"}
    return {"token": token}
