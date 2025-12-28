import os
import pandas as pd
import time
from googleapiclient.discovery import build
from dotenv import load_dotenv 
from datetime import datetime
from models.schema import VideoMetrics
from dataclasses import asdict
from dataclasses import asdict
from db.models import Video
from db.session import save_videos_db
from utils.logger import logger
from ingest.base import safe_execute
from utils.normalize import normalize_metrics


load_dotenv() 

def get_youtube_client():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY environment variable not set")
    return build("youtube", "v3", developerKey=api_key)

def get_channel_info(youtube, channel_id):
    response = safe_execute(youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    ), platform ="YouTube")

    item = response["items"][0]
    
    return{
        "creator_id": channel_id,
        "creator_name": item["snippet"]["title"],
        "subscriber_count": int(item["statistics"]["subscriberCount"]),
    }

def get_recent_videos(youtube, channel_id, maxResults=100):
    video_ids = []
    next_page_token = None

    while len(video_ids) < maxResults:
        response = safe_execute(youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=min(50, maxResults - len(video_ids)),
            order="date",
            type="video",
            pageToken=next_page_token
        ), platform ="YouTube")

        for item in response["items"]:
            video_ids.append(item["id"]["videoId"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return video_ids

def get_video_metrics(youtube, video_ids, creator_id, creator_name):
    response = safe_execute(youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    ), platform ="YouTube")
    videos = []
    for item in response["items"]:
        stats = item.get("statistics", {})
        snippet = item["snippet"]
        videos.append(
            normalize_metrics(
                VideoMetrics(
                platform="YouTube",
                creator_id=creator_id,
                creator_name=creator_name,
                video_id=item["id"],
                title=snippet["title"],
                published_at=datetime.strptime(snippet["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
                views=int(stats.get("viewCount", 0)),
                likes=int(stats.get("likeCount", 0)),
                comments=int(stats.get("commentCount", 0)),
            )
        ))

    logger.info(f"Fetched {len(videos)} videos from YouTube")
    return videos

def save_videos_to_csv(videos, filename):
    df = pd.DataFrame([asdict(video) for video in videos])
    df.to_csv(filename, index=False)

def ingest_youtube_channel(channel_id):
    youtube = get_youtube_client()

    channel_info = get_channel_info(youtube, channel_id)
    video_ids = get_recent_videos(youtube, channel_id, maxResults=100)
    videos = get_video_metrics(
        youtube,
        video_ids,
        channel_info["creator_id"],
        channel_info["creator_name"]
    )
    db_videos = [
        Video(**asdict(video)) for video in videos
    ]
    save_videos_db(db_videos)
