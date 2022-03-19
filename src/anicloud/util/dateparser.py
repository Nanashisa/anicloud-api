import datetime
import re


def parse(s: str) -> datetime.datetime:
    reg = re.search(r"(?P<day>[0-9]{1,2})\.(?P<month>[0-9]{1,2})\.(?P<year>[0-9]{4})\s+(?P<hour>[0-9]{1,"
                    r"2}):(?P<minute>[0-9]{1,2})", s)
    return datetime.datetime(int(reg.group("year")),
                             int(reg.group("month")),
                             int(reg.group("day")),
                             int(reg.group("hour")),
                             int(reg.group("minute")))
