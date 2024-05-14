from fastapi import APIRouter, Response
from passlib.context import CryptContext
from schemas.generic import ResponseMsg
from schemas.posts import PostInfo, PostComment, PostList

import sqlite3
from datetime import datetime

router = APIRouter(prefix="/post")
con = sqlite3.connect("friendbook.db")


@router.post("/")
async def create_post(post: PostInfo, response: Response) -> ResponseMsg:

    try:
        cur = con.cursor()
        if post.img_url != None:
            cur.execute(
                """INSERT INTO posts(user_id, content, img_url, created_at)
                VALUES(?,?,?,?)""",
                [post.user_id, post.post_texts, post.img_url, datetime.now()],
            )

        else:
            cur.execute(
                """INSERT INTO posts(user_id, content, created_at)
                VALUES(?,?,?)""",
                [post.user_id, post.post_texts, datetime.now()],
            )
        con.commit()
        return ResponseMsg(msg="Post published")

    except sqlite3.IntegrityError as e:
        response.status_code = 400
        return ResponseMsg(msg=f"Error occurred: {str(e)}")


@router.put("/{post_id}")
async def edit_post(post: PostInfo, response: Response) -> ResponseMsg:
    post_edited_at = datetime.now()
    try:
        cur = con.cursor()
        cur.execute(
            """UPDATE posts
                SET content = ?,
                img_url = ?, 
                edited_at = ?
                WHERE post_id = ?""",
            [post.post_texts, post.img_url, post_edited_at, post.post_id],
        )
        con.commit()
        return ResponseMsg(msg="Post edited")
    except sqlite3.IntegrityError as e:
        response.status_code = 400
        return ResponseMsg(msg=f"Error occurred: {str(e)}")


@router.delete("/{post_id}")
async def delete_post(post_id: int, response: Response) -> ResponseMsg:
    try:
        cur = con.cursor()
        cur.execute("SELECT post_id from posts WHERE post_id = ?", [post_id])
        res = cur.fetchone()
        if not res:
            response.status_code = 404
            return ResponseMsg(msg="Post not found")
        else:
            cur.execute("DELETE from posts WHERE post_id = ?", [post_id])
            con.commit()

    except sqlite3.IntegrityError as e:
        response.status_code = 400
        return ResponseMsg(msg=f"Error occurred: {str(e)}")

    return ResponseMsg(msg="Post deleted")


@router.get("/{user_id}")
async def get_post(user_id: int, response: Response) -> list[PostList]:
    cur = con.cursor()
    cur.execute(
        """SELECT 
        posts.post_id, u.user_id, u.firstname, u.lastname, u.username, u.profile_img_url, 
        posts.content, posts.img_url, posts.created_at, posts.edited_at
        FROM posts
        JOIN users u ON posts.user_id = u.user_id
        WHERE posts.user_id = ?
        """,
        [user_id],
    )
    res = cur.fetchall()
    posts_list = [
        PostList(
            post_id=row[0],
            user_id=row[1],
            user_fullname=" ".join([row[2], row[3]]),
            username=row[4],
            user_profile_img=row[5],
            post_content=row[6],
            post_img=row[7],
            post_created_at=row[8],
            post_edited_at=row[9],
        )
        for row in res
    ]

    return posts_list


@router.post("/toggle_like/{post_id}")
async def like_post(user_id: int, post_id: int, response: Response) -> ResponseMsg:
    cur = con.cursor()
    cur.execute(
        "SELECT post_id FROM user_liked_posts WHERE user_liked_posts.user_id = ? AND  user_liked_posts.post_id = ? ",
        [user_id, post_id],
    )
    res = cur.fetchall()
    if not res:
        cur.execute(
            """INSERT INTO user_liked_posts (user_id, post_id, timestamp) VALUES(?,?,?)""",
            [user_id, post_id, datetime.now()],
        )
        con.commit()
        return ResponseMsg(msg="Post Liked")

    else:
        cur.execute(
            "DELETE from user_liked_posts WHERE user_liked_posts.user_id = ? AND user_liked_posts.post_id = ? ",
            [user_id, post_id],
        )
        con.commit()
        return ResponseMsg(msg="Post Unliked")


@router.post("/comment/{post_id}")
async def add_post_comment(comment: PostComment, response: Response) -> ResponseMsg:
    created_at = datetime.now()
    try:
        cur = con.cursor()
        cur.execute(
            """INSERT INTO post_comments(post_id,user_id,content,created_at)
                        VALUES (?,?,?,?)""",
            [comment.post_id, comment.user_id, comment.content, created_at],
        )
        con.commit()
    except sqlite3.IntegrityError as e:
        response.status_code = 400
        return ResponseMsg(msg=f"Error occurred: {str(e)}")

    return ResponseMsg(msg="Comment added")


@router.delete("/comment/{comment_id}")
async def delete_post_comment(comment_id: int, response: Response) -> ResponseMsg:
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM post_comments WHERE comment_id = ?", [comment_id])
        con.commit()

        if cur.rowcount == 0:
            response.status_code = 404
            return ResponseMsg(msg="Comment id not found")

    except sqlite3.IntegrityError as e:
        response.status_code = 400
        return ResponseMsg(msg=f"Error occurred: {str(e)}")

    return ResponseMsg(msg=f"Comment deleted (comment id: {comment_id})")
