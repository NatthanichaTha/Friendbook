from pydantic import BaseModel
from datetime import datetime


# CREATE TABLE friendships (
#     friendship_id INTEGER PRIMARY KEY,
#     sender_id INTEGER,
#     receiver_id INTEGER,
#     status VARCHAR(20),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (sender_id) REFERENCES users(user_id),
#     FOREIGN KEY (receiver_id) REFERENCES users(user_id)
# );
# sender_id: User ID of the user who sent the friend request.
# receiver_id: User ID of the user who will receive the friend request.
# status: Status of the friendship (e.g., "pending", "accepted", "rejected").
# created_at: Timestamp indicating when the friendship request was created.


class FriendshipInfo(BaseModel):
    friendship_id: int = None
    sender_id: int
    receiver_id: int
    status: str = "pending"
    created_at: datetime = None


class FriendRequesterInfo(BaseModel):
    user_id: int
    fullname: str
    profile_img_url: str


class FriendInfo(BaseModel):
    user_id: int
    fullname: str
    profile_img_url: str
