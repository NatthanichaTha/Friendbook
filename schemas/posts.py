from pydantic import BaseModel
from datetime import datetime


class PostInfo(BaseModel):
    post_id: int = None
    user_id: int
    post_texts: str
    img_url: str = None
    created_at: str = None
    edited_at: str = None


class PostComment(BaseModel):
    comment_id: int = None
    post_id: int
    user_id: int
    content: str
    created_at: str | None = None


class PostList(BaseModel):
    post_id: int
    user_id: int
    user_fullname: str
    username: str | None = None
    user_profile_img: str | None = None
    post_content: str | None = None
    post_img: str | None = None
    post_created_at: str
    post_edited_at: str | None = None
