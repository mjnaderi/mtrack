import signal
import sys
import time

import sh

from mtrack.database import init_db
from mtrack.models import Project, TimeEntry
from mtrack.utils import now, get_idle_time, format_datetime, format_duration


class MTrackTimer:
    IDLE_THRESHOLD = 5 * 60  # 5 minutes

    def __init__(self, project_name):
        init_db()
        self.project_name = project_name
        self.project = Project.get_or_create_project(project_name)

    def run(self):
        time_entry = TimeEntry.start_timer(self.project.id)

        def signal_handler(sig, frame):
            TimeEntry.save_finish_time(time_entry.id, now())
            self.exit()

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
                    # print('you were idle')
                    if selection == 1:
                        TimeEntry.save_finish_time(time_entry.id, last_activity)
                        time_entry = TimeEntry.start_timer(self.project.id)
                    elif selection == 2:
                        TimeEntry.save_finish_time(time_entry.id, last_activity)
                        self.exit()
                    idle = False
                last_activity = now()
                TimeEntry.save_finish_time(time_entry.id, last_activity)
            time.sleep(2)

    # noinspection PyUnresolvedReferences
    def ask_idle(self, last_activity):
        selection = None
        while selection is None:
            idle_duration = now() - last_activity
            text = 'You were idle for <b>{}</b> (since {})\nProject: <b>{}</b>'.format(
                format_duration(idle_duration),
                format_datetime(last_activity),
                self.project_name,
            )
            try:
                selection = int(sh.zenity('--height=220', '--list', '--title=MTrack: You were idle', '--text=%s' % text,
                                          '--column=#', '--column=Select an option', '--hide-column=1',
                                          '1', 'Discard time and continue',
                                          '2', 'Discard time and stop',
                                          '3', 'Keep time').strip())
            except (sh.ErrorReturnCode_1, ValueError):
                selection = None
        return selection

    @staticmethod
    def exit():
        print('Good Bye!')
        sys.exit(0)
