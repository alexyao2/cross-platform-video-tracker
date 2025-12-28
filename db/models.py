from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Video (Base):
    __tablename__ = "videos"
    video_id = Column(String, primary_key = True)
    platform = Column(String)
    creator_id = Column(String)
    creator_name = Column(String)
    title = Column(String)
    published_at = Column(DateTime)
    views = Column(Integer)
    likes = Column(Integer)
    comments = Column(Integer)
    engagement_rate = Column(Integer)