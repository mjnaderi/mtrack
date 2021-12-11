import subprocess
from datetime import datetime

import pytz
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
    if (
        p := subprocess.run(["xprintidle"], capture_output=True, text=True)
    ).returncode == 0:
        return int(p.stdout) / 1000

    # https://askubuntu.com/a/1231995/123230
    if (
        p := subprocess.run(
            [
                "dbus-send",
                "--print-reply",
                "--dest=org.gnome.Mutter.IdleMonitor",
                "/org/gnome/Mutter/IdleMonitor/Core",
                "org.gnome.Mutter.IdleMonitor.GetIdletime",
            ],
            capture_output=True,
            text=True,
        )
    ).returncode == 0:
        return int(p.stdout.rsplit(None, 1)[-1]) / 1000

    return 0


def format_duration(duration):
    def _format(l):
        result = []
        for a, b in l:
            if b == 0:
                continue
            if b == 1:
                result.append("1 " + a)
            else:
                result.append("%d %ss" % (b, a))
            if len(result) >= 2:
                break
        return ", ".join(result)

    ss = int(duration.total_seconds())
    s = ss % 60
    mm = ss // 60
    m = mm % 60
    hh = mm // 60
    h = hh % 24
    d = hh // 24
    return _format([("day", d), ("hour", h), ("minute", m), ("second", s)])


def format_datetime(dt):
    return dt.astimezone(get_localzone()).strftime("%Y-%b-%d %H:%M:%S")
