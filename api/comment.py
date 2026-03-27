"""댓글 API 엔드포인트"""

from db.connection import execute_query


def get_comments(post_id: int) -> list[dict]:
    rows = execute_query(
        "SELECT id, author_id, content, created_at FROM comments WHERE post_id=%s ORDER BY created_at",
        (post_id,),
    )
    return [{"id": r[0], "author_id": r[1], "content": r[2], "created_at": r[3]} for r in rows]


def create_comment(post_id: int, author_id: int, content: str) -> dict:
    if not content.strip():
        return {"error": "댓글 내용을 입력해주세요."}
    execute_query(
        "INSERT INTO comments (post_id, author_id, content) VALUES (%s, %s, %s)",
        (post_id, author_id, content),
    )
    return {"post_id": post_id, "author_id": author_id, "content": content}


def delete_comment(comment_id: int, requester_id: int) -> dict:
    rows = execute_query(
        "SELECT author_id FROM comments WHERE id=%s", (comment_id,)
    )
    if not rows:
        return {"error": "댓글을 찾을 수 없습니다."}
    if rows[0][0] != requester_id:
        return {"error": "삭제 권한이 없습니다."}
    execute_query("DELETE FROM comments WHERE id=%s", (comment_id,))
    return {"deleted": comment_id}
