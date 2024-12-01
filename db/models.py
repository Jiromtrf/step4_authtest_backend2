# models.py

from sqlalchemy import Column, Integer, String
from db.database import Base  # 相対インポート

# ユーザーマスターテーブル
class UserMaster(Base):
    __tablename__ = "user_master"

    user_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

# ステータステーブル
class StatusTable(Base):
    __tablename__ = "status_table"

    user_id = Column(String(50), primary_key=True, index=True)
    biz = Column(Integer, nullable=False)
    design = Column(Integer, nullable=False)
    tech = Column(Integer, nullable=False)
