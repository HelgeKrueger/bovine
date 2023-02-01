from datetime import datetime, timedelta, timezone

from dateutil.parser import parse


def get_gmt_now() -> str:
    return datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")


def parse_gmt(date_string: str) -> datetime:
    return parse(date_string)


def check_max_offset_now(dt: datetime, minutes: int = 5) -> bool:
    now = datetime.now(tz=timezone.utc)

    if dt > now + timedelta(minutes=minutes):
        return False

    if dt < now - timedelta(minutes=minutes):
        return False

    return True
