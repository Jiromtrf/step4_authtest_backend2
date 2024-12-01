# init_db.py

from バックエンド.db.database import engine
from models import Base

def init_db():
    Base.metadata.create_all(bind=engine)
    print("データベースの初期化が完了しました。")

if __name__ == "__main__":
    init_db()
