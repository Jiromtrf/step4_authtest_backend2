from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db.database import get_db, engine
from db.models import UserMaster, StatusTable

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

# リクエストボディ用モデル
class LoginRequest(BaseModel):
    user_id: str
    password: str

# ログイン用エンドポイント
@app.post("/api/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        # ユーザIDで検索
        user = db.query(UserMaster).filter(UserMaster.user_id == request.user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid user ID or password")

        # パスワードのチェック
        if not pwd_context.verify(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid user ID or password")

        return {"message": "Login successful", "user_id": user.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# スキルデータ取得用エンドポイント
@app.get("/api/user/skills")
def get_user_skills(user_id: str, db: Session = Depends(get_db)):
    try:
        # ユーザー情報とスキルデータを結合して取得
        user = db.query(UserMaster).filter(UserMaster.user_id == user_id).first()
        status = db.query(StatusTable).filter(StatusTable.user_id == user_id).first()

        if not user or not status:
            raise HTTPException(
                status_code=404,
                detail=f"User skills not found for user_id: {user_id}"
            )

        skill_data = {
            "name": user.name,
            "biz": status.biz,
            "design": status.design,
            "tech": status.tech
        }

        return skill_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
