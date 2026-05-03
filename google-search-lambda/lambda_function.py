import json
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def lambda_handler(event, context):
    query = event.get("query", "AWS Lambda")
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"

    logger.info("Sending request to Google Search | query=%s | url=%s", query, url)

    response = requests.get(url, headers=HEADERS, timeout=10)

    logger.info(
        "Response received with message | status=%d | size_bytes=%d",
        response.status_code,
        len(response.content),
    )

    return {
        "statusCode": response.status_code,
        "query": query,
        "responseSize": len(response.content),
    }
