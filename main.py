import uvicorn
import sqlite3
from fastapi import FastAPI

from routes.users import router as users_router
from routes.posts import router as posts_router

app = FastAPI()
# include routers
app.include_router(users_router)
app.include_router(posts_router)


con = sqlite3.connect("friendbook.db")


def init_db():
    cur = con.cursor()
    cur.execute(
        """ 
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            hashed_password TEXT,
            firstname TEXT, 
            lastname TEXT,
            phone_no TEXT,
            birthday TEXT,
            gender TEXT,
            profile_img_url TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS posts(
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT,
        img_url TEXT,  
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        edited_at DATETIME,
        FOREIGN KEY (user_id) REFERENCES users(user_id)       
        )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS post_comments(
        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        user_id INTEGER,
        content TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (post_id) REFERENCES posts(post_id)
        )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS user_liked_posts(
        user_id INTEGER,
        post_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (post_id) REFERENCES posts(post_id),
        PRIMARY KEY (user_id, post_id)
        )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS friendships(
        friendship_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id_1 INTEGER,
        user_id_2 INTEGER,
        status TEXT,
        created_at DATETIME,
        accepted_at DATETIME,
        FOREIGN KEY (user_id_1) REFERENCES users(user_id),
        FOREIGN KEY (user_id_2) REFERENCES users(user_id),
        UNIQUE (user_id_1, user_id_2)
        )"""
    )

    con.commit()


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
