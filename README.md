# yt-shorts-downloader

A small Python script that downloads videos with [yt-dlp](https://github.com/yt-dlp/yt-dlp). Tested with YouTube (videos and Shorts), Instagram Reels and TikTok. yt-dlp supports many other sites too.

## Setup

Requires Python 3.10+, `ffmpeg`, and `deno` (YouTube needs a JS runtime). On macOS:

```bash
brew install ffmpeg deno
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

## Usage

```bash
venv/bin/python download.py "<video-url>"
```

Options:

| Flag | Description |
| --- | --- |
| `-o`, `--output-dir` | Folder to save into (default: current directory) |
| `--cookies-from-browser` | Browser to read login cookies from (default: `chrome`; also `safari`, `firefox`, `edge`, or `''` to disable) |

Examples:

```bash
venv/bin/python download.py "https://www.youtube.com/shorts/VIDEO_ID"
venv/bin/python download.py "https://www.instagram.com/reels/REEL_ID/" -o ~/Downloads
venv/bin/python download.py "https://www.tiktok.com/@user/video/1234567890"
```

Files are saved as `<title>.mp4`.

## Notes

- **Login cookies:** YouTube and Instagram often require you to be signed in. Log in to the site in Chrome first; the script reads those cookies (macOS may ask for Keychain access).
- **Use the page URL:** `blob:` URLs copied from a browser won't work. Use the video's normal link (for TikTok, Share > Copy link).
- **Playback compatibility:** VP9 and AV1 video in an mp4 plays as audio-only in QuickTime/Safari, so the script re-encodes those to H.264 with ffmpeg automatically.
- **Playlists:** a link containing `&list=...` downloads the whole playlist.
- **If a download breaks:** sites change often. Try `venv/bin/pip install -U yt-dlp`.
- Only download content you have the right to save.
