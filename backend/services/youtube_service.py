"""YouTube transcript fetcher using youtube-transcript-api."""

import re

from youtube_transcript_api import YouTubeTranscriptApi


def _extract_video_id(url: str) -> str:
    """Extract the YouTube video ID from various URL formats.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://youtube.com/shorts/VIDEO_ID

    Raises:
        ValueError: If the video ID cannot be extracted.
    """
    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"shorts/([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url!r}")


async def fetch_transcript(url: str) -> str:
    """Fetch the transcript of a YouTube video as plain text.

    Args:
        url: Full YouTube video URL.

    Returns:
        Concatenated transcript text.

    Raises:
        ValueError: If the URL is invalid or the transcript is unavailable.
    """
    video_id = _extract_video_id(url)
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join(entry["text"] for entry in transcript_list)
