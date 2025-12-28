import time
from googleapiclient.errors import HttpError
from utils.logger import logger


def safe_execute(request, platform: str, retries: int = 3):
    for attempt in range(retries):
        try:
            return request.execute()
        except HttpError as e:
            logger.warning(
                f"[{platform}] API error (attempt {attempt + 1}/{retries}): {e}"
            )
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
        except Exception as e:
            logger.exception(f"[{platform}] Unexpected error")
            raise
