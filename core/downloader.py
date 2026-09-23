import os
import sys
import glob
import re
import subprocess
import importlib
import yt_dlp
from .config import AppConfig

class MediaDownloader:
    """Encapsulates media extraction and downloading using yt-dlp and ffmpeg."""

    DESKTOP_RELEASE_URL = "https://github.com/remonedward/REMO_OX-Downloader/releases/download/v2.0/REMO_OX_Downloader_v2.exe"

    def __init__(self):
        self.temp_dir = AppConfig.ensure_temp_dir()
        self.ffmpeg_path = AppConfig.get_ffmpeg_path()

    @staticmethod
    def get_engine_version():
        """Returns the current yt-dlp version."""
        try:
            return yt_dlp.version.__version__
        except Exception:
            return "Unknown"

    @classmethod
    def upgrade_engine(cls):
        """Updates yt-dlp to the latest release directly from PyPI."""
        try:
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            global yt_dlp
            yt_dlp = importlib.reload(yt_dlp)
            new_version = yt_dlp.version.__version__
            
            return True, new_version, result.stdout
        except Exception as e:
            return False, cls.get_engine_version(), str(e)

    def download(self, url, is_audio=False, quality="1080p", *args, **kwargs):
        """
        Downloads and merges media from Instagram, TikTok, Facebook, Twitter, and other platforms.
        """
        # Guard for YouTube links
        if 'youtube.com' in url.lower() or 'youtu.be' in url.lower():
            return False, None, None, None, "YOUTUBE_RESTRICTED"

        opts = {
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            'geo_bypass': True,
            'outtmpl': os.path.join(self.temp_dir, '%(id)s.%(ext)s'),
        }

        if self.ffmpeg_path:
            opts['ffmpeg_location'] = self.ffmpeg_path

        # 1. Format configuration
        if is_audio:
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            quality_map = {
                "1080p": "1080",
                "720p": "720",
                "480p": "480",
                "360p": "360",
                "Best Available": "best"
            }
            res_val = quality_map.get(quality, quality)
            if res_val != "best":
                opts['format'] = f"bestvideo[height<={res_val}]+bestaudio/best[height<={res_val}]/best"
            else:
                opts['format'] = 'bestvideo+bestaudio/best'

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if not info:
                    return False, None, None, None, "Could not extract video metadata."

                media_id = info.get('id', '')
                title = info.get('title', 'downloaded_media')
                clean_title = re.sub(r'[\\/*?:"<>|]', "", title)

                # Locate the downloaded file by media_id
                found_files = []
                for fname in os.listdir(self.temp_dir):
                    if fname.startswith(f"{media_id}.") and not fname.endswith(".part") and not fname.endswith(".ytdl"):
                        full_path = os.path.join(self.temp_dir, fname)
                        if os.path.isfile(full_path) and os.path.getsize(full_path) > 0:
                            found_files.append(full_path)

                if not found_files:
                    return False, None, None, None, "The downloaded file is empty or could not be found."

                # Pick the latest non-empty file
                downloaded_file = max(found_files, key=os.path.getmtime)
                file_ext = os.path.splitext(downloaded_file)[1].lstrip('.')
                final_name = f"{clean_title}.{file_ext}"
                mime_type = "audio/mpeg" if file_ext == "mp3" else f"video/{file_ext}"

                return True, downloaded_file, final_name, mime_type, None

        except Exception as e:
            return False, None, None, None, str(e)
