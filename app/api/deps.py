from app.core.database import SessionLocal


def create_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = [
    "create_db_session"
]
