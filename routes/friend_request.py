from fastapi import APIRouter, Response
from schemas.generic import ResponseMsg
from schemas.friends import FriendRequesterInfo

import sqlite3
from datetime import datetime

router = APIRouter(prefix="/friend-request")
con = sqlite3.connect("friendbook.db")


@router.get("/{user_id}")
async def get_friend_requests(
    user_id: int, response: Response
) -> list[FriendRequesterInfo]:
    cur = con.cursor()
    cur.execute(
        """
                SELECT u.user_id, u.firstname, u.lastname, u.profile_img_url 
                FROM friendships f
                JOIN users u ON (f.user_id_1 = u.user_id OR f.user_id_2 = u.user_id)
                WHERE f.user_id_2 = ? AND f.status = ? ORDER BY f.created_at""",
        [user_id, "pending"],
    )
    res = cur.fetchall()
    friend_requesters = [
        FriendRequesterInfo(
            user_id=row[0],
            user_fullname=" ".join([row[1], row[2]]),
            profile_img_url=row[3],
        )
        for row in res
    ]
    return friend_requesters


@router.post("/")
async def send_friend_request(
    sender_user_id: int, receiver_user_id: int, response: Response
) -> ResponseMsg:
    try:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO friendships(user_id_1, user_id_2, status, created_at) VALUES (?,?,?,?)",
            [sender_user_id, receiver_user_id, "Pending", datetime.now()],
        )
        con.commit()
        return ResponseMsg(msg="Friend request sent")

    except sqlite3.IntegrityError as e:
        response.status_code = 400
        return ResponseMsg(msg=f"Error occurred: {str(e)}")


@router.put("/")
async def reply_friend_request(
    receiver_user_id: int, sender_user_id: int, accept: bool, response: Response
) -> ResponseMsg:
    timestamp = datetime.now()
    try:
        cur = con.cursor()
        cur.execute(
            """UPDATE friendships 
            SET user_id_1 = ?,
            user_id_2 = ?,
            status = ?,
            accepted_at = ?""",
            [sender_user_id, receiver_user_id, "Accepted", datetime.now()],
        )
        con.commit()
        return ResponseMsg(msg="Friend request accepted")

    except sqlite3.IntegrityError as e:
        response.status_code = 400
        return ResponseMsg(msg=f"Error occurred: {str(e)}")
