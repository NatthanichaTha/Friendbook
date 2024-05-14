from fastapi import APIRouter, Response
from passlib.context import CryptContext
from schemas.generic import ResponseMsg
from schemas.users import (
    SignUpInfo,
    Credentials,
    ProfileInfo,
    UpdateCredentials,
    LoginToken,
)
import sqlite3
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


router = APIRouter(prefix="/users")
con = sqlite3.connect("friendbook.db")


@router.post("/register")
async def register_user(info: SignUpInfo, response: Response) -> ResponseMsg:
    hashed_pwd = get_password_hash(info.password)
    try:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO users(email, hashed_password, firstname, lastname, created_at)
            VALUES (?,?,?,?,?)
            """,
            [info.email, hashed_pwd, info.firstname, info.lastname, datetime.now()],
        )
        con.commit()
    except sqlite3.IntegrityError as e:
        response.status_code = 400
        return ResponseMsg(msg=f"Error occurred: {str(e)}")

    return ResponseMsg(msg="Registration completed")


@router.post("/username/{user_id}")
async def set_username(
    user_id: int, inserted_username: str, response: Response
) -> ResponseMsg:
    cur = con.cursor()
    cur.execute("SELECT username from users WHERE username = ?", [inserted_username])
    res = cur.fetchone()
    if not res:
        cur.execute(
            "UPDATE users SET username = ? WHERE user_id = ?",
            [inserted_username, user_id],
        )
        con.commit()
        return ResponseMsg(msg="Username updated")
    else:
        return ResponseMsg(msg="This username is already exists")


@router.post("/login")
async def login(info: Credentials, response: Response) -> ResponseMsg:
    cur = con.cursor()
    cur.execute(
        """
        SELECT hashed_password, email, user_id 
        from users
        WHERE users.email = ?
        """,
        [info.email],
    )
    res = cur.fetchone()
    if not res:
        response.status_code = 404
        return ResponseMsg(msg="Email address not found")
    hashed_password = res[0]
    if verify_password(info.inserted_password, hashed_password):
        return ResponseMsg(msg="Login success")
    else:
        response.status_code = 400
        return ResponseMsg(msg="Password not matched")

    # return user_id and token as LoginToken


@router.get("/logout")
async def logout(user_id: int, response: Response) -> ResponseMsg:

    pass


@router.get("/profile/{user_id}")
async def get_profile(user_id: int, response: Response) -> list[ProfileInfo]:
    cur = con.cursor()
    cur.execute(
        """
                SELECT user_id, username, email, firstname, lastname,
                phone_no, birthday, gender, profile_img_url,
                created_at
                FROM users
                WHERE user_id = ? """,
        [user_id],
    )
    res = cur.fetchall()
    profile_info = [
        ProfileInfo(
            user_id=row[0],
            username=row[1],
            email=row[2],
            firstname=row[3],
            lastname=row[4],
            phone_no=row[5],
            birthday=row[6],
            gender=row[7],
            profile_img_url=row[8],
            created_at=row[9],
        )
        for row in res
    ]
    return profile_info


@router.put("/profile")
async def update_profile(info: ProfileInfo, response: Response) -> ResponseMsg:
    try:
        cur = con.cursor()
        cur.execute(
            """
                UPDATE users
                SET firstname = ?, 
                lastname =? ,
                phone_no = ?,
                birthday = ?,
                gender = ?,
                profile_img_url = ?
                WHERE user_id = ? """,
            [
                info.firstname,
                info.lastname,
                info.phone_no,
                info.birthday,
                info.gender,
                info.profile_img_url,
                info.user_id,
            ],
        )
        con.commit()

    except sqlite3.IntegrityError as e:
        response.status_code = 400
        return ResponseMsg(msg=f"Error occurred: {str(e)}")

    return ResponseMsg(msg="Profile edited")


@router.put("/change-password")
async def change_password(info: UpdateCredentials, response: Response) -> ResponseMsg:
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT hashed_password FROM users WHERE user_id = ?", [info.user_id]
        )
        res = cur.fetchone()
        if res is None:
            return ResponseMsg(msg="User id not exists")
        curr_hashed_pwd = res[0]
        if verify_password(info.current_pwd, curr_hashed_pwd):
            new_hashed_pwd = get_password_hash(info.new_pwd)
            cur.execute(
                "UPDATE users set hashed_password = ? WHERE user_id = ?",
                [new_hashed_pwd, info.user_id],
            )
            con.commit()
            return ResponseMsg(msg="Password changed")
        else:
            return ResponseMsg(msg="Incorrect password")
    except sqlite3.IntegrityError as e:
        response.status_code = 400
        return ResponseMsg(msg=f"Error occurred: {str(e)}")


# check if username already exists
@router.get("/check-username")
async def check_username(username: str, response: Response) -> ResponseMsg:
    cur = con.cursor()
    cur.execute("SELECT username from users WHERE username = ?", [username])
    res = cur.fetchone()
    if not res:
        return ResponseMsg(msg="Username available")
    else:
        return ResponseMsg(msg="This username is already exists")
