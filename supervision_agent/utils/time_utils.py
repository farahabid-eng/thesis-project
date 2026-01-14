from datetime import datetime

def get_now() -> datetime:
    """Returns current UTC time."""
    return datetime.utcnow()
