#!/usr/bin/env python3
"""Download a YouTube video (including Shorts) given its URL."""

import argparse
import os
import subprocess
import sys

import yt_dlp


def ensure_h264(path: str) -> None:
    """Re-encode to H.264 if needed; VP9/AV1 in mp4 plays as audio-only in QuickTime/Safari."""
    codec = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name",
         "-of", "csv=p=0", path],
        capture_output=True, text=True,
    ).stdout.strip()
    if codec in ("", "h264", "hevc"):
        return
    print(f"Re-encoding {codec} -> h264 for compatibility...")
    tmp = path + ".h264.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-c:v", "libx264", "-crf", "18",
         "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", tmp],
        check=True,
    )
    os.replace(tmp, path)


def download(url: str, output_dir: str = ".", cookies_from_browser: str | None = "chrome") -> None:
    ydl_opts = {
        "format": "bv*+ba/b",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        # YouTube now requires solving a JS challenge to get download URLs;
        # this lets yt-dlp fetch the (cached) solver script instead of failing.
        "remote_components": ["ejs:github"],
        # The default clients sometimes only expose a 360p combined stream;
        # mweb also returns the separate high-res video/audio streams.
        "extractor_args": {"youtube": {"player_client": ["default", "mweb"]}},
    }
    if cookies_from_browser:
        ydl_opts["cookiesfrombrowser"] = (cookies_from_browser,)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        path = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp4"
    ensure_h264(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a YouTube video/short.")
    parser.add_argument("url", help="YouTube video or Shorts URL")
    parser.add_argument(
        "-o", "--output-dir", default=".", help="Directory to save the video (default: current directory)"
    )
    parser.add_argument(
        "--cookies-from-browser",
        default="chrome",
        help="Browser to pull cookies from for sign-in (default: chrome; use safari, firefox, edge, or '' to disable)",
    )
    args = parser.parse_args()

    try:
        download(args.url, args.output_dir, args.cookies_from_browser)
    except yt_dlp.utils.DownloadError as e:
        print(f"Download failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
