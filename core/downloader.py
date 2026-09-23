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

    def download(self, url, is_audio=False, quality="1080p", cookies_browser="none", client_mode="auto", cookies_text=None, *args, **kwargs):
        """
        Downloads and merges media using the exact proven logic from the desktop app.
        Accepts any argument variation to prevent Streamlit hot-reload TypeErrors.
        """
        opts = {
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            'geo_bypass': True,
            'outtmpl': os.path.join(self.temp_dir, '%(id)s.%(ext)s'),
            'js_runtimes': {'node': {}},
        }

        try:
            from yt_dlp.networking.impersonate import ImpersonateTarget
            opts['impersonate'] = ImpersonateTarget.from_str('chrome')
        except Exception:
            pass

        if self.ffmpeg_path:
            opts['ffmpeg_location'] = self.ffmpeg_path

        is_youtube = ('youtube.com' in url.lower() or 'youtu.be' in url.lower())

        # 1. Format configuration (Prioritizing HLS m3u8 for YouTube to prevent 403 on cloud servers)
        if is_audio:
            if is_youtube:
                opts['format'] = 'bestaudio[protocol^=m3u8]/bestaudio/best'
            else:
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
            if is_youtube:
                if res_val != "best":
                    opts['format'] = f"bestvideo[height<={res_val}][protocol^=m3u8]+bestaudio[protocol^=m3u8]/bestvideo[height<={res_val}]+bestaudio/best[height<={res_val}]/best"
                else:
                    opts['format'] = "bestvideo[protocol^=m3u8]+bestaudio[protocol^=m3u8]/bestvideo+bestaudio/best"
            else:
                if res_val != "best":
                    opts['format'] = f"bestvideo[height<={res_val}]+bestaudio/best"
                else:
                    opts['format'] = 'bestvideo+bestaudio/best'

        # 2. Browser cookies or cookies file
        cookies_file = None
        if cookies_text and len(cookies_text.strip()) > 10:
            cookies_file = os.path.join(self.temp_dir, "session_cookies.txt")
            with open(cookies_file, "w", encoding="utf-8") as f:
                f.write(cookies_text.strip())
            opts['cookiefile'] = cookies_file
        elif cookies_browser and str(cookies_browser).lower() != 'none':
            try:
                browser_name = str(cookies_browser).lower()
                browser_dirs = {
                    'chrome': os.path.expanduser('~/.config/google-chrome'),
                    'edge': os.path.expanduser('~/.config/microsoft-edge'),
                    'firefox': os.path.expanduser('~/.mozilla/firefox'),
                    'brave': os.path.expanduser('~/.config/BraveSoftware'),
                    'opera': os.path.expanduser('~/.config/opera'),
                }
                # On Windows desktop it exists in AppData, but on headless cloud container ignore if missing
                if os.name == 'nt' or os.path.exists(browser_dirs.get(browser_name, '')):
                    opts['cookiesfrombrowser'] = (browser_name, )
            except Exception:
                pass

        # 3. Client bypass mode
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
                'youtube': {'player_client': ['web_embedded', 'web']}
            }
        else:
            # Smart Auto (Recommended) - VisionOS + Android ensures 0 403 Forbidden errors on cloud
            opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['visionos', 'android', 'mweb', 'web_creator'],
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
            elif "video is unavailable" in err_msg.lower() or "unavailable" in err_msg.lower() or "not available" in err_msg.lower():
                err_msg = "هذا الفيديو غير متاح على يوتيوب (قد يكون محذوفاً أو خاصاً)."
            return False, None, None, None, err_msg
        finally:
            if cookies_file and os.path.exists(cookies_file):
                try:
                    os.remove(cookies_file)
                except Exception:
                    pass
