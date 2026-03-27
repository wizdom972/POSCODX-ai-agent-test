"""인증 모듈 테스트"""

from auth.login import hash_password
from auth.jwt_handler import create_token, verify_token


def test_hash_password():
    assert hash_password("password123") == hash_password("password123")
    assert hash_password("abc") != hash_password("xyz")


def test_create_and_verify_token():
    token = create_token(user_id=1, username="testuser")
    payload = verify_token(token)
    assert payload["sub"] == 1
    assert payload["username"] == "testuser"
