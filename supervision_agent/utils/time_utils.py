from datetime import datetime

class TimeUtils:
    @staticmethod
    def now_str() -> str:
        return datetime.now().isoformat()
        
    @staticmethod
    def format_duration(seconds: int) -> str:
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes}m {seconds}s"
