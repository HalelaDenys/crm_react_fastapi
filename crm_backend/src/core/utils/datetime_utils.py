from datetime import datetime, date, time, timezone
from typing import Optional


def make_utc_datetime(d: date, end_of_day: bool = False) -> Optional[datetime]:
    """
    Converts the `date` object to `datetime` with the UTC time zone.
    """
    if d is None:
        return None
    t = time.max if end_of_day else time.min
    return datetime.combine(d, t).replace(tzinfo=timezone.utc)
