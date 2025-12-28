from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from db.models import Video

engine = create_engine("sqlite:///videos.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

def save_videos_db(videos):
    session = SessionLocal()
    try:
        for video in videos:
            session.merge(video)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()