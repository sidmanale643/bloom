#!/usr/bin/env python3
"""Fetch a YouTube transcript and write it directly to inbox/.

Usage:
    uvx --from youtube-transcript-api python3 scripts/bloom-youtube.py <youtube_url>

Writes the raw transcript text to inbox/<Video Title>.md.
Prints the output path to stdout on success.
"""

import json
import re
import sys
import urllib.request
from pathlib import Path


def extract_video_id(url):
    patterns = [
        r"(?:youtube\.com/watch\?v=)([^&]+)",
        r"(?:youtu\.be/)([^?&]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_title(url):
    oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
    with urllib.request.urlopen(oembed_url) as resp:
        data = json.loads(resp.read())
    return data.get("title", "Untitled")


def get_transcript(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    try:
        transcript = api.fetch(video_id, languages=["en"])
    except Exception:
        transcript_list = api.list(video_id)
        codes = [t.language_code for t in transcript_list]
        transcript = api.fetch(video_id, languages=codes)
    return " ".join(snippet.text for snippet in transcript)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: uvx --from youtube-transcript-api python3 scripts/bloom-youtube.py <youtube_url>",
            file=sys.stderr,
        )
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)
    if not video_id:
        print(f"Error: could not extract video ID from {url}", file=sys.stderr)
        sys.exit(1)

    title = get_title(url)

    try:
        transcript = get_transcript(video_id)
    except Exception as e:
        print(f"Error: could not fetch transcript for {video_id}: {e}", file=sys.stderr)
        sys.exit(1)

    vault_root = Path(__file__).resolve().parent.parent
    inbox_dir = vault_root / "inbox"
    inbox_dir.mkdir(exist_ok=True)

    safe_title = title.replace("/", "-").strip()
    filepath = inbox_dir / f"{safe_title}.md"
    filepath.write_text(transcript, encoding="utf-8")

    print(str(filepath))


if __name__ == "__main__":
    main()