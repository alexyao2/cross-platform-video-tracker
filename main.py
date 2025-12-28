import argparse
from ingest.youtube import ingest_youtube_channel
from ingest.tiktok import ingest_tiktok_user
from db.session import engine
from db.models import Base


def main():
    parser = argparse.ArgumentParser(
        description="Cross-platform video ingestion CLI"
    )
    parser.add_argument(
        "platform",
        choices=["youtube", "tiktok"],
        help="Platform to ingest data from"
    )
    parser.add_argument("--channel-id", help="YouTube channel ID")
    parser.add_argument("--username", help="TikTok username")
    args = parser.parse_args()
    Base.metadata.create_all(engine)

    if args.platform == "youtube":
        if not args.channel_id:
            parser.error("--channel-id is required for YouTube")
        ingest_youtube_channel(args.channel_id)
    elif args.platform == "tiktok":
        if not args.username:
            parser.error("--username is required for TikTok")
        ingest_tiktok_user(args.username)

if __name__ == "__main__":
    main()
