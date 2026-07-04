import json
import os
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_API_URL = os.getenv("TAVILY_API_URL", "https://api.tavily.ai/v1/trends")

_cache: dict[str, tuple[list[dict[str, str]], float]] = {}


def _normalize_item(item) -> dict[str, str] | None:
    if isinstance(item, dict):
        content = item.get("content") or item.get("title") or item.get("headline") or item.get("summary") or item.get("description")
        url = item.get("url") or item.get("link") or item.get("source_url")
        title = item.get("title") or item.get("headline") or item.get("source") or "Live context"
        if content:
            return {"content": str(content).strip(), "url": str(url).strip() if url else "", "title": str(title).strip()}
    elif item is not None:
        return {"content": str(item).strip(), "url": "", "title": "Live context"}
    return None


def fetch_tavily_context(topic: str, ttl: int = 3600) -> list[dict[str, str]] | None:
    """Fetch trending context for a topic using Tavily and cache results per topic."""
    if not topic or not TAVILY_API_KEY:
        return None

    normalized_topic = topic.strip().lower()
    now = time.time()
    cached = _cache.get(normalized_topic)
    if cached and now - cached[1] < ttl:
        return cached[0]

    query = urllib.parse.quote(topic)
    url = f"{TAVILY_API_URL}?query={query}&scope=news&days=7&limit=3"
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Accept": "application/json",
        "User-Agent": "LinkedIn-Post-Generator/1.0",
    }
    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            raw = response.read().decode("utf-8")
            payload = json.loads(raw)
    except (HTTPError, URLError, json.JSONDecodeError):
        return None

    sources: list[dict[str, str]] = []
    if isinstance(payload, dict):
        for key in ("trends", "results", "data", "items", "entries"):
            items = payload.get(key)
            if isinstance(items, list) and items:
                for item in items[:3]:
                    normalized = _normalize_item(item)
                    if normalized:
                        sources.append(normalized)
                if sources:
                    break

        if not sources:
            message = payload.get("message") or payload.get("trend")
            if isinstance(message, str):
                normalized = _normalize_item({"content": message, "title": "Live context"})
                if normalized:
                    sources.append(normalized)

    if not sources:
        return None

    _cache[normalized_topic] = (sources, now)
    return sources
