from datetime import datetime, timezone

def months_ago(iso_date):
    if iso_date == None:
        return None
    released = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    month_amount = (now - released).days // 30
    return month_amount

