#!/usr/bin/env python3
import argparse
import logging
import signal
import sys
import time

import sh
from pony import orm
from tzlocal import get_localzone

from mtrack.database import init_db
from mtrack.models import Project, TimeInterval
from mtrack.utils import now, ask_idle
from mtrack.version import __version__

IDLE_THRESHOLD = 5  # 5 minutes


@orm.db_session
def get_or_create_project(project_name):
    p, created = Project.get_or_create(name=project_name)
    if created:
        print(f'Created project {project_name}')
    return p


@orm.db_session
def create_interval(project_id):
    return TimeInterval(project=project_id, start=now())


@orm.db_session
def finish_interval(interval_id, dt):
    interval = TimeInterval[interval_id]
    interval.finish = dt
    return interval


def main():
    parser = argparse.ArgumentParser(description='mtrack')
    parser.add_argument('--version', action='version', version=f'MTrack {__version__}')
    parser.add_argument('project', help='project name')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('sh.command').setLevel(logging.WARNING)
    init_db()
    p = get_or_create_project(args.project)
    i = create_interval(p.id)

    def signal_handler(sig, frame):
        print('Good Bye!')
        finish_interval(i.id, now())
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    idle = False
    last_activity = now()
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
            last_activity = now()
            finish_interval(i.id, last_activity)
        time.sleep(10)


if __name__ == "__main__":
    main()
