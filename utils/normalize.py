import pandas as pd
from db.session import SessionLocal
from db.models import Video
from utils.logger import logger

def normalize_metrics(video):
    video.engagement_rate = round(
        (video.likes + video.comments) / max(video.views, 1), 
        4
    ) 
    return video