from pydantic import BaseModel
from datetime import date
from typing import Optional


class SignUpInfo(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str


class Credentials(BaseModel):
    email: str
    inserted_password: str


class ProfileInfo(BaseModel):
    user_id: int
    username: Optional[str] = None
    email: Optional[str] = None
    firstname: str
    lastname: str
    phone_no: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[str] = None
    profile_img_url: Optional[str] = None
    created_at: Optional[str] = None


class UpdateCredentials(BaseModel):
    user_id: int
    current_pwd: str
    new_pwd: str


class LoginToken(BaseModel):
    user_id: int
    token: dict
