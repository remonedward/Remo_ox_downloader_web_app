import os
import glob
import re
import yt_dlp
from .config import AppConfig

class MediaDownloader:
    """Encapsulates media extraction and downloading using yt-dlp and ffmpeg."""

    def __init__(self):
        self.temp_dir = AppConfig.ensure_temp_dir()
        self.ffmpeg_path = AppConfig.get_ffmpeg_path()

    def get_base_options(self):
        """Builds standard robust extraction options."""
        opts = {
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            'geo_bypass': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'web_creator', 'tv_embedded', 'mweb'],
                }
            }
        }
        if self.ffmpeg_path:
            opts['ffmpeg_location'] = self.ffmpeg_path
        return opts

    def extract_info(self, url):
        """Fetches metadata without downloading."""
        opts = self.get_base_options()
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
            if "confirm you're not a bot" in err.lower():
                err = "BOT_DETECTED"
            return {'success': False, 'error': err}

    def download(self, url, is_audio=False, quality="Best Available"):
        """Downloads and converts media file, returning its path and metadata."""
        opts = self.get_base_options()
        
        # Output template with safe ASCII/sanitized filename
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
            # Map quality
            quality_map = {
                "1080p": "1080",
                "720p": "720",
                "480p": "480",
                "360p": "360"
            }
            res_limit = quality_map.get(quality)
            if res_limit:
                opts['format'] = f"bestvideo[height<={res_limit}]+bestaudio/best[height<={res_limit}]/best"
            else:
                opts['format'] = 'bestvideo+bestaudio/best'

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'downloaded_media')
                # Clean title for saving
                clean_title = re.sub(r'[\\/*?:"<>|]', "", title)

                # Locate the newly downloaded file
                target_ext = 'mp3' if is_audio else info.get('ext', 'mp4')
                downloaded_file = None
                
                # Check directly prepared filename
                expected_fn = ydl.prepare_filename(info)
                if is_audio:
                    base, _ = os.path.splitext(expected_fn)
                    expected_fn = base + ".mp3"
                
                if os.path.exists(expected_fn):
                    downloaded_file = expected_fn
                else:
                    # Search by ID in temp dir
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
            if "confirm you're not a bot" in err.lower():
                err = "BOT_DETECTED"
            return False, None, None, None, err
