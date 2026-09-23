import os
import sys
import glob
import re
import subprocess
import importlib
import yt_dlp
from .config import AppConfig

class MediaDownloader:
    """Encapsulates media extraction, downloading, and engine updates using yt-dlp and ffmpeg."""

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

    def download(self, url, is_audio=False, quality="1080p", cookies_browser="none", client_mode="auto"):
        """
        Downloads and merges media using the exact proven logic from the desktop app.
        """
        opts = {
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            'geo_bypass': True,
            'outtmpl': os.path.join(self.temp_dir, '%(id)s.%(ext)s'),
        }

        if self.ffmpeg_path:
            opts['ffmpeg_location'] = self.ffmpeg_path

        # 1. Format configuration identical to desktop app
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
                opts['format'] = f"bestvideo[height<={res_val}]+bestaudio/best"
            else:
                opts['format'] = 'bestvideo+bestaudio/best'

        # 2. Browser cookies identical to desktop app
        if cookies_browser and cookies_browser.lower() != 'none':
            try:
                opts['cookiesfrombrowser'] = (cookies_browser.lower(), )
            except Exception:
                pass

        # 3. Client bypass mode identical to desktop app
        if client_mode == 'ios':
            opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['ios'],
                    'player_skip': ['webpage', 'configs']
                }
            }
        elif client_mode == 'android':
            opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['android'],
                    'player_skip': ['webpage', 'configs']
                }
            }
        elif client_mode == 'web':
            opts['extractor_args'] = {
                'youtube': {'player_client': ['web']}
            }
        else:
            # Smart Auto (Recommended) - Exact desktop extractor args
            opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['ios', 'android', 'web_creator', 'tv_embedded', 'mweb'],
                }
            }

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
            err_msg = str(e)
            if "confirm you're not a bot" in err_msg.lower() or "sign in" in err_msg.lower():
                err_msg = "BOT_DETECTED"
            return False, None, None, None, err_msg
