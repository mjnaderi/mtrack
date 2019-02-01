from datetime import datetime
import pytz
import sh


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