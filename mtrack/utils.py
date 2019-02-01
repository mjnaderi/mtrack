from datetime import datetime

import pytz
import sh
from tzlocal import get_localzone


class GetOrCreateMixin:
    @classmethod
    def get_or_create(cls, **kwargs):
        o = cls.get(**kwargs)
        if o is None:
            return cls(**kwargs), True
        else:
            return o, False


def now():
    return datetime.utcnow().replace(tzinfo=pytz.utc)


def get_idle_time():
    # noinspection PyUnresolvedReferences
    return int(sh.xprintidle().strip()) / 1000  # in seconds


def format_duration(duration):
    def _format(l):
        result = []
        for a, b in l:
            if b == 0:
                continue
            if b == 1:
                result.append('1 ' + a)
            else:
                result.append('%d %ss' % (b, a))
            if len(result) >= 2:
                break
        return ', '.join(result)

    ss = int(duration.total_seconds())
    s = ss % 60
    mm = ss // 60
    m = mm % 60
    hh = mm // 60
    h = hh % 24
    d = hh // 24
    return _format([('day', d), ('hour', h), ('minute', m), ('second', s)])


def format_datetime(dt):
    return dt.astimezone(get_localzone()).strftime('%Y-%b-%d %H:%M:%S')
