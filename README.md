# Cross-Platform Video Tracker

A data engineering pipeline to ingest, normalize, and compare engagement metrics across **YouTube** and **TikTok**.

## Features
* **Dual Ingestion**: YouTube Data API + Playwright-backed TikTok scraping.
* **Unified Schema**: Normalizes platform-specific data into a single SQLite database.
* **Smart Analytics**: Calculates normalized engagement rates for fair comparison.
* **CLI Driven**: Simple commands to trigger platform syncs.

## Project Structure
```
├── ingest/     # YouTube API & TikTok Scraper logic
├── db/         # SQLAlchemy models & SQLite sessions
├── models/     # Unified VideoMetrics schema
├── utils/      # Logger & Engagement normalization
└── main.py     # CLI Entry point
```

## Setup
```
1. install: pip install -r requirements.txt && playwright install chromium.
2. env.: Be sure to modify .env with your YouTube API key and proxy credentials, or it will
   not run!
```

## Usage
```bash
# Sync YouTube Channel
python main.py youtube --channel-id <CHANNEL_ID>

# Sync TikTok Creator
python mian.py tiktok --username <USERNAME>
```

## Disclaimer
```
TikTok ingestion uses unofficial scraping via Playwright. It handles rate limits and browser 
challenges gracefully, but requires a proxy for consistent results.
```

## Output
```
Running the ingestion commands produces a unified SQLite database (videos.db) containing 
normalized engagement metrics from both YouTube and TikTok.
Each record includes basic metadata (platform, creator, video ID), raw engagement metrics 
(views, likes, comments), and a normalized engagement rate: (likes + comments) / views.
```