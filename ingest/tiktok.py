import asyncio
import os
from TikTokApi import TikTokApi
from datetime import datetime
from dataclasses import asdict
from models.schema import VideoMetrics
from db.models import Video
from db.session import save_videos_db
from utils.logger import logger
from dotenv import load_dotenv
from utils.normalize import normalize_metrics

async def _ingest_tiktok_async(username: str, limit: int):
    logger.info(f"Starting TikTok ingestion for @{username}")
    load_dotenv()
    server = os.getenv("TIKTOK_PROXY_SERVER")
    usernm = os.getenv("TIKTOK_PROXY_USER")
    pwd = os.getenv("TIKTOK_PROXY_PASS")
    api = TikTokApi()
    
    try:
        await api.create_sessions(
            num_sessions=1,
            sleep_after=5,
            browser="chromium",
            headless=False,
            proxies=[{
                "server": server, 
                "username": usernm,
                "password": pwd
            }], 
            context_options={
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
        )
        videos = []
        user = api.user(username=username)

        async for video in user.videos(count=limit):
            video_dict = video.as_dict
            stats = video_dict.get("stats", {})
            videos.append(
                normalize_metrics(
                    VideoMetrics(
                        platform="TikTok",
                        creator_id=username,
                        creator_name=username,
                        video_id=video_dict.get("id"),
                        title=video_dict.get("desc", "")[:100],
                        published_at=datetime.fromtimestamp(
                            video_dict.get("createTime", 0)
                        ),
                        views=int(stats.get("playCount", 0)),
                        likes=int(stats.get("diggCount", 0)),
                        comments=int(stats.get("commentCount", 0)),
                    )
                )
            )
        db_videos = [Video(**asdict(v)) for v in videos]
        save_videos_db(db_videos)
        logger.info(f"TikTok ingestion complete: {len(videos)} videos")

    except Exception:
        logger.exception("TikTok ingestion failed")
        raise
    finally:
        await api.close_sessions()
        await api.stop_playwright()

def ingest_tiktok_user(username: str, limit: int = 30):
    asyncio.run(_ingest_tiktok_async(username, limit))
