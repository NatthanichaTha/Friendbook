from fastapi import APIRouter, Response
from schemas.generic import ResponseMsg
from schemas.friends import FriendInfo

import sqlite3
from datetime import datetime

router = APIRouter(prefix="/friend")
con = sqlite3.connect("friendbook.db")


@router.get("/{user_id}")
async def get_friend_requests(user_id: int, response: Response) -> list[FriendInfo]:
    pass


@router.delete("/{user_id}")
async def remove_friend(
    user_id: int, friend_id: int, response: Response
) -> ResponseMsg:
    pass
