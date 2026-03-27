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
    status: str = "draft"          # 새 필드: 게시 상태 (draft/published/deleted)
    view_count: int = 0            # 새 필드: 조회수
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Comment:
    id: int
    post_id: int
    author_id: int
    content: str
    created_at: datetime = field(default_factory=datetime.now)
