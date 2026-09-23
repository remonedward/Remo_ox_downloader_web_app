import os
import shutil

class AppConfig:
    """Application configuration and environment settings."""
    APP_NAME = "Remo_ox_downloader_web_app"
    DISPLAY_NAME = "REMO_OX Downloader Web"
    VERSION = "v0.1"
    AUTHOR = "Remon Edward"
    
    # Base and Temp paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMP_DIR = os.path.join(BASE_DIR, "temp_downloads")
    
    # Supported qualities
    VIDEO_QUALITIES = ["1080p", "720p", "480p", "360p", "Best Available"]
    FORMAT_TYPES = ["Video (MP4)", "Audio (MP3)"]
    
    # Max file age in minutes for cleaner
    MAX_TEMP_AGE_MINUTES = 30

    @classmethod
    def ensure_temp_dir(cls):
        """Ensures that the temporary downloads directory exists."""
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
        return cls.TEMP_DIR

    @classmethod
    def get_ffmpeg_path(cls):
        """
        Locates ffmpeg executable:
        1. Checks system PATH (default on Linux / Streamlit Cloud).
        2. Checks local bin/ directory (in case running on Windows desktop).
        """
        system_ffmpeg = shutil.which("ffmpeg")
        if system_ffmpeg:
            return system_ffmpeg
        
        # Check parent bin folder on Windows
        parent_bin = os.path.join(os.path.dirname(cls.BASE_DIR), "bin", "ffmpeg.exe")
        if os.path.exists(parent_bin):
            return parent_bin
            
        local_bin = os.path.join(cls.BASE_DIR, "bin", "ffmpeg.exe")
        if os.path.exists(local_bin):
            return local_bin

        return None
