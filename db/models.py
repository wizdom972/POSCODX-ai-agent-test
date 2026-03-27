"""데이터베이스 모델 정의"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Post:
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime = field(default_factory=datetime.now)
