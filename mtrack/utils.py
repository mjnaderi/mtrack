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


# noinspection PyUnresolvedReferences
def ask_idle(last_activity):
    selection = None
    while selection is None:
        idle_duration = now() - last_activity
        text = f'You were idle for {idle_duration} (since {last_activity})'
        try:
            selection = int(sh.zenity('--list', '--title=You were idle', f'--text={text}',
                                      '--column=#', '--column=Choice',
                                      '1', 'Discard time and continue',
                                      '2', 'Discard time and stop',
                                      '3', 'Keep time').strip())
        except (sh.ErrorReturnCode_1, ValueError):
            selection = None
    return selection
