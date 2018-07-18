import pytz

from bson.timestamp import Timestamp
from dateutil.parser import parse


def utc_datetime(obj):
    if isinstance(obj, str):
        obj = parse(obj)
    if not obj.tzinfo:
        obj = pytz.UTC.localize(obj)
    else:
        obj = obj.astimezone(pytz.UTC)
    return obj


def utc_timestamp(string):
    date = utc_datetime(string)
    return Timestamp(date, 1)
