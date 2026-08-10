import re
from urllib.parse import parse_qs, urlparse


def youtube_video_id(url):
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.hostname in {"youtu.be", "www.youtu.be"}:
        return parsed.path.lstrip("/").split("/")[0]
    if parsed.hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [""])[0]
        match = re.match(r"^/(embed|shorts|live)/([^/?]+)", parsed.path)
        if match:
            return match.group(2)
    return ""


def vimeo_video_id(url):
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.hostname in {"vimeo.com", "www.vimeo.com", "player.vimeo.com"}:
        parts = [part for part in parsed.path.split("/") if part]
        if parts:
            return parts[-1]
    return ""


def video_embed_url(url):
    youtube_id = youtube_video_id(url)
    if youtube_id:
        return f"https://www.youtube.com/embed/{youtube_id}"
    vimeo_id = vimeo_video_id(url)
    if vimeo_id:
        return f"https://player.vimeo.com/video/{vimeo_id}"
    return ""


def video_thumbnail_url(url):
    youtube_id = youtube_video_id(url)
    if youtube_id:
        return f"https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg"
    return ""
