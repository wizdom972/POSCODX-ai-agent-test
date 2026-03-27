"""데이터베이스 연결 관리"""

import psycopg2
from config.settings import DATABASE


def get_connection():
    return psycopg2.connect(
        host=DATABASE["host"],
        port=DATABASE["port"],
        dbname=DATABASE["name"],
        user=DATABASE["user"],
    )


def execute_query(query: str, params: tuple = ()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.fetchall()
    finally:
        conn.close()
