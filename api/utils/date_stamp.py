from datetime import datetime, timezone

def date_stamp():
    return datetime.now(timezone.utc).isoformat()