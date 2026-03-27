"""게시글 API 엔드포인트"""

from db.connection import execute_query


def get_posts(page: int = 1, size: int = 10) -> list[dict]:
    offset = (page - 1) * size
    rows = execute_query(
        "SELECT id, title, author_id, created_at FROM posts LIMIT %s OFFSET %s",
        (size, offset),
    )
    return [{"id": r[0], "title": r[1], "author_id": r[2], "created_at": r[3]} for r in rows]


def create_post(title: str, content: str, author_id: int) -> dict:
    execute_query(
        "INSERT INTO posts (title, content, author_id) VALUES (%s, %s, %s)",
        (title, content, author_id),
    )
    return {"title": title, "author_id": author_id}
