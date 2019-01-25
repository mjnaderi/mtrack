#!/usr/bin/env python3
import argparse
import os
import signal
import sys
import time
from datetime import datetime

import sh
from pony import orm
from tzlocal import get_localzone
from version import __version__

IDLE_THRESHOLD = 5 * 60  # 5 minutes


class GetOrCreateMixin:
    @classmethod
    def get_or_create(cls, **kwargs):
        o = cls.get(**kwargs)
        if o is None:
            return cls(**kwargs), True
        else:
            return o, False


db = orm.Database()


class Project(db.Entity, GetOrCreateMixin):
    name = orm.Required(str)
    time_intervals = orm.Set('TimeInterval')


class TimeInterval(db.Entity):
    project = orm.Required(Project)
    start = orm.Required(datetime)
    finish = orm.Optional(datetime)


DATA_DIR = os.path.expanduser('~/.mtrack')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
DB_FILE = os.path.join(DATA_DIR, 'db.sqlite')
db.bind(provider='sqlite', filename=DB_FILE, create_db=True)
db.generate_mapping(create_tables=True)


@orm.db_session
def get_or_create_project(project_name):
    p, created = Project.get_or_create(name=project_name)
    if created:
        print(f'Created project {project_name}')
    return p


@orm.db_session
def create_interval(project_id):
    return TimeInterval(project=project_id, start=datetime.now())


@orm.db_session
def finish_interval(interval_id, dt):
    interval = TimeInterval[interval_id]
    interval.finish = dt
    return interval


# noinspection PyUnresolvedReferences
def ask_idle(last_activity):
    selection = None
    while selection is None:
        idle_duration = datetime.now() - last_activity
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


def main():
    parser = argparse.ArgumentParser(description='mtrack')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('project', help='project name')
    args = parser.parse_args()
    p = get_or_create_project(args.project)
    i = create_interval(p.id)
    # print(i.start)

    def signal_handler(sig, frame):
        print('Good Bye!')
        finish_interval(i.id, datetime.now())
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    idle = False
    last_activity = datetime.now()
    while True:
        # noinspection PyUnresolvedReferences
        idle_time = int(sh.xprintidle().strip()) / 1000  # in seconds
        if idle_time > IDLE_THRESHOLD:
            if not idle:
                idle = True
        elif idle_time < 20:
            if idle:
                selection = ask_idle(last_activity)
                if selection == 1:
                    finish_interval(i.id, last_activity)
                    i = create_interval(p.id)
                elif selection == 2:
                    finish_interval(i.id, last_activity)
                    sys.exit(0)
                print('you were idle')
                idle = False
            last_activity = datetime.now()
            finish_interval(i.id, last_activity)
        time.sleep(10)


if __name__ == "__main__":
    main()
