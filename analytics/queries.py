from db.session import SessionLocal
from db.models import Video
from sqlalchemy import func

def avg_engagement_by_platform():
    session = SessionLocal()
    results = (
        session.query(
            Video.platform,
            func.avg(Video.engagement_rate)
        )
        .group_by(Video.platform).all()
    )
    session.close()
    return results

def top_videos():
    session = SessionLocal()
    results = (
        session.query(Video)
        .order_by(Video.engagement_rate.desc())
        .limit(10)
        .all()
    )
    session.close()
    return results
