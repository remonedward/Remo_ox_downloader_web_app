import os
import time
from .config import AppConfig

class TempCleaner:
    """Manages temporary files cleanup to prevent server disk overflow."""
    
    @classmethod
    def clean_old_files(cls, max_age_minutes=AppConfig.MAX_TEMP_AGE_MINUTES):
        temp_dir = AppConfig.ensure_temp_dir()
        current_time = time.time()
        max_age_seconds = max_age_minutes * 60
        removed_count = 0
        
        try:
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age_seconds:
                        try:
                            os.remove(file_path)
                            removed_count += 1
                        except Exception:
                            pass
        except Exception:
            pass
            
        return removed_count

    @classmethod
    def clear_all(cls):
        temp_dir = AppConfig.ensure_temp_dir()
        removed_count = 0
        try:
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        removed_count += 1
                    except Exception:
                        pass
        except Exception:
            pass
        return removed_count
