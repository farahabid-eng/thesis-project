from datetime import datetime

def get_now() -> datetime:
    return datetime.now()

def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%%d %H:%M:%S")

def get_duration_seconds(start: datetime, end: datetime) -> float:
    return (end - start).total_seconds()
