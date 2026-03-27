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
class Tag:
    id: int
    name: str       # 태그명 (예: "python", "공지사항")
    slug: str       # URL 슬러그 (예: "python", "notice")


@dataclass
class Post:
    id: int
    title: str
    content: str
    author_id: int
    status: str = "draft"
    view_count: int = 0
    tags: list = field(default_factory=list)   # Tag ID 목록
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Comment:
    id: int
    post_id: int
    author_id: int
    content: str
    parent_id: int | None = None    # 대댓글 지원
    created_at: datetime = field(default_factory=datetime.now)
