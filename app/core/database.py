from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# 创建数据库引擎，启用连接池
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#  声明式基类, 所有的数据库模型类都要继承自这个基类
DatabaseBaseModel = declarative_base()

__all__ = [
    "engine",
    "SessionLocal",
    "DatabaseBaseModel"
]
