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
        """
        Updates yt-dlp to the latest release directly from PyPI/GitHub.
        Works both locally and in web environments.
        """
        try:
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            # Reload module dynamically in runtime
            global yt_dlp
            yt_dlp = importlib.reload(yt_dlp)
            new_version = yt_dlp.version.__version__
            
            return True, new_version, result.stdout
        except Exception as e:
            return False, cls.get_engine_version(), str(e)

    def get_base_options(self, cookies_file=None, client_mode="auto"):
        """
        Builds standard robust extraction options that bypass 403 Forbidden.
        Avoids forcing ios client which requires GVS PO Token.
        """
        opts = {
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            'geo_bypass': True,
            'retries': 5,
            'fragment_retries': 5,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            }
        }
        
        # Extractor arguments based on client mode
        if client_mode == "tv":
            opts['extractor_args'] = {'youtube': {'player_client': ['tv_embedded', 'web_embedded']}}
        elif client_mode == "android":
            opts['extractor_args'] = {'youtube': {'player_client': ['android', 'web']}}
        elif client_mode == "web":
            opts['extractor_args'] = {'youtube': {'player_client': ['web']}}
        else:
            # Smart Auto: Let yt-dlp pick best unblocked client (VisionOS, Web, etc.)
            opts['extractor_args'] = {'youtube': {'player_skip': ['configs']}}

        if self.ffmpeg_path:
            opts['ffmpeg_location'] = self.ffmpeg_path

        if cookies_file and os.path.exists(cookies_file):
            opts['cookiefile'] = cookies_file

        return opts

    def extract_info(self, url, cookies_file=None, client_mode="auto"):
        """Fetches metadata without downloading."""
        opts = self.get_base_options(cookies_file=cookies_file, client_mode=client_mode)
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'success': True,
                    'title': info.get('title', 'Media'),
                    'thumbnail': info.get('thumbnail', ''),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'id': info.get('id', '')
                }
        except Exception as e:
            err = str(e)
            if "confirm you're not a bot" in err.lower() or "sign in" in err.lower():
                err = "BOT_DETECTED"
            return {'success': False, 'error': err}

    def download(self, url, is_audio=False, quality="Best Available", cookies_text=None, client_mode="auto"):
        """Downloads and converts media file, returning its path and metadata."""
        cookies_file = None
        if cookies_text and len(cookies_text.strip()) > 10:
            cookies_file = os.path.join(self.temp_dir, "session_cookies.txt")
            with open(cookies_file, "w", encoding="utf-8") as f:
                f.write(cookies_text.strip())

        opts = self.get_base_options(cookies_file=cookies_file, client_mode=client_mode)
        
        # Output template with safe sanitized filename
        output_template = os.path.join(self.temp_dir, '%(id)s_%(epoch)s.%(ext)s')
        opts['outtmpl'] = output_template

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
                "360p": "360"
            }
            res_limit = quality_map.get(quality)
            if res_limit:
                opts['format'] = f"(bestvideo[height<={res_limit}]+bestaudio/best[height<={res_limit}])/best"
            else:
                opts['format'] = '(bestvideo+bestaudio)/best'

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'downloaded_media')
                clean_title = re.sub(r'[\\/*?:"<>|]', "", title)

                # Locate the newly downloaded file
                target_ext = 'mp3' if is_audio else info.get('ext', 'mp4')
                downloaded_file = None
                
                expected_fn = ydl.prepare_filename(info)
                if is_audio:
                    base, _ = os.path.splitext(expected_fn)
                    expected_fn = base + ".mp3"
                
                if os.path.exists(expected_fn):
                    downloaded_file = expected_fn
                else:
                    media_id = info.get('id', '')
                    matches = glob.glob(os.path.join(self.temp_dir, f"{media_id}_*.*"))
                    if matches:
                        downloaded_file = max(matches, key=os.path.getmtime)

                if not downloaded_file or not os.path.exists(downloaded_file):
                    return False, None, None, None, "File was processed but could not be located on disk."

                file_ext = os.path.splitext(downloaded_file)[1].lstrip('.')
                final_name = f"{clean_title}.{file_ext}"
                mime_type = "audio/mpeg" if is_audio else f"video/{file_ext}"

                return True, downloaded_file, final_name, mime_type, None

        except Exception as e:
            err = str(e)
            if "confirm you're not a bot" in err.lower() or "sign in" in err.lower():
                err = "BOT_DETECTED"
            return False, None, None, None, err
        finally:
            if cookies_file and os.path.exists(cookies_file):
                try:
                    os.remove(cookies_file)
                except Exception:
                    pass
