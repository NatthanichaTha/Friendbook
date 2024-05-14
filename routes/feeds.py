from fastapi import APIRouter, Response
from passlib.context import CryptContext
from schemas.generic import ResponseMsg
from schemas.user import SignUpInfo, Credentials, ProfileInfo, UpdateCredentials
import sqlite3

router = APIRouter(prefix="/features")
con = sqlite3.connect("friendbook.db")

# GET /feed: Endpoint to view the user's feed containing posts from friends.


# POST /share: Endpoint to share a post.
