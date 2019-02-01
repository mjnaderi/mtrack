import sys

import signal
import time
import sh

from mtrack.database import init_db
from mtrack.models import Project, TimeEntry
from mtrack.utils import now, get_idle_time
from tzlocal import get_localzone


class MTrackTimer:
    IDLE_THRESHOLD = 5  # 5 minutes

    def __init__(self, project_name):
        init_db()
        self.project_name = project_name
        self.project = Project.get_or_create_project(project_name)

    def run(self):
        time_entry = TimeEntry.start_timer(self.project.id)

        def signal_handler(sig, frame):
            print('Good Bye!')
            TimeEntry.stop_timer(time_entry.id, now())
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        idle = False
        last_activity = now()
        while True:
            idle_time = get_idle_time()
            if idle_time > self.IDLE_THRESHOLD:
                if not idle:
                    idle = True
            elif idle_time < 20:
                if idle:
                    selection = self.ask_idle(last_activity)
                    if selection == 1:
                        TimeEntry.stop_timer(time_entry.id, last_activity)
                        time_entry = TimeEntry.start_timer(self.project.id)
                    elif selection == 2:
                        TimeEntry.stop_timer(time_entry.id, last_activity)
                        sys.exit(0)
                    print('you were idle')
                    idle = False
                last_activity = now()
                TimeEntry.stop_timer(time_entry.id, last_activity)
            time.sleep(2)

    # noinspection PyUnresolvedReferences
    def ask_idle(self, last_activity):
        selection = None
        while selection is None:
            idle_duration = now() - last_activity
            text = 'Project <b>{}</b>\nYou were idle for {} (since {})'.format(
                self.project_name, idle_duration, last_activity
            )
            try:
                selection = int(sh.zenity('--list', '--title=You were idle', '--text=%s' % text,
                                          '--column=#', '--column=Choice',
                                          '1', 'Discard time and continue',
                                          '2', 'Discard time and stop',
                                          '3', 'Keep time').strip())
            except (sh.ErrorReturnCode_1, ValueError):
                selection = None
        return selection