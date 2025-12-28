from dataclasses import dataclass
from datetime import datetime

@dataclass
class VideoMetrics:
    platform: str
    creator_id: str
    creator_name: str
    video_id: str
    title: str
    published_at: datetime
    views: int
    likes: int
    comments: int
    engagement_rate: float = 0.0 
    