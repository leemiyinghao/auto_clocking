import os
from datetime import datetime, timedelta
from typing import Optional

import psutil
import urllib.request

from auto_clocking.models import Clock

def is_slack_exist() -> bool:
    return (
        next(
            filter(lambda process: process.name() == "Slack", psutil.process_iter()),
            None,
        )
        is not None
    )

def get_ip_addr() -> str:
    ''' Get public IPv4 address'''
    try:
        ip_addr = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
        return ip_addr
    except:
        pass
    return ''

def log_activity(now: Optional[datetime] = None, ip_addr: Optional[str] = None) -> None:
    now = now or datetime.now()
    ip_addr = ip_addr or get_ip_addr()
    date = now.date()
    # turn date back in datetime format
    date = datetime(year=date.year, month=date.month, day=date.day)
    interval: int = int(os.getenv("INTERVAL", 5))
    last_log: Optional[Clock] = (
        Clock.select()
        .where(Clock.at >= max(date, now - timedelta(minutes=interval*2)))
        .order_by(Clock.at.desc())
        .get_or_none()
    )
    if last_log:
        if last_log.session_begin:
            Clock.insert(at=now, ip_addr=ip_addr, session_begin=False).execute()
        else:
            last_log.at = now  # type: ignore
            last_log.save()
    else:
        Clock.insert(at=now, ip_addr=ip_addr, session_begin=True).execute()


def dump_activities(days_ago: int) -> list[tuple[datetime, str, str]]:
    _begin = datetime.now().date() - timedelta(days=days_ago)
    return [
        (clock.at, clock.ip_addr, "clock-in" if clock.session_begin else "clock-out")
        for clock in Clock.select().where(Clock.at >= _begin).iterator()
    ]
