from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import mysql.connector
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import os

# パスワードハッシュ化の設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI アプリの作成
app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて変更
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB接続設定
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("tech0-gen-7-step4-studentrdb-1.mysql.database.azure.com", "localhost"),
        user=os.environ.get("tech0gen7student", "root"),
        password=os.environ.get("F4XyhpicGw6P", ""),
        database=os.environ.get("app_db", "app_db")
    )

# リクエストボディ用モデル
class LoginRequest(BaseModel):
    user_id: str
    password: str

# レスポンスモデル
class SkillData(BaseModel):
    user_id: str
    biz: int
    design: int
    tech: int

# ログイン用エンドポイント
@app.post("/api/auth/login")
def login(request: LoginRequest):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # ユーザIDで検索
        cursor.execute("SELECT * FROM user_master WHERE user_id = %s", (request.user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid user ID or password")

        # パスワードのチェック
        if not pwd_context.verify(request.password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid user ID or password")

        return {"message": "Login successful", "user_id": user["user_id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# スキルデータ取得用エンドポイント
@app.get("/api/user/skills", response_model=dict)
def get_user_skills(user_id: str):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # ユーザー情報とスキルデータを結合して取得
        cursor.execute(
            """
            SELECT um.name, st.biz, st.design, st.tech
            FROM user_master um
            JOIN status_table st ON um.user_id = st.user_id
            WHERE um.user_id = %s
            """,
            (user_id,)
        )
        skill_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if not skill_data:
            raise HTTPException(
                status_code=404,
                detail=f"User skills not found for user_id: {user_id}"
            )

        return skill_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


