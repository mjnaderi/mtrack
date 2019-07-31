from datetime import datetime, timedelta
from pony import orm

from mtrack.color_print import Color, cprint
from mtrack.database import init_db
from mtrack.jalali import jalali_to_gregorian, gregorian_to_jalali
from mtrack.models import Project, TimeEntry


class MTrackReporter:

    def __init__(self, project_name, date):
        init_db()
        self.project_name = project_name
        jy = int(date[0])
        jm = int(date[1])
        self.start_time = datetime(*jalali_to_gregorian(jy, jm, 1))
        jm += 1
        if jm == 13:
            jm = 1
            jy += 1
        self.finish_time = datetime(*jalali_to_gregorian(jy, jm, 1))

    @orm.db_session
    def report(self, just_time):
        project = Project.get(name=self.project_name)
        time_entries = TimeEntry.select(
            lambda t: t.start >= self.start_time and t.start < self.finish_time and t.project == project
        ).order_by(lambda t: t.start)

        print("----------------------------")
        self.print_table(time_entries, just_time)
        print("----------------------------")
        total_time = self.total_time(time_entries)
        print(
            "Total: {:02d}:{:02d}".format(
                total_time.days * 24 + total_time.seconds // 3600,
                (total_time.seconds // 60) % 60
            )
        )

    @staticmethod
    @orm.db_session
    def total_time(time_entries):
        return sum([time_entry.finish - time_entry.start for time_entry in time_entries], timedelta())

    @staticmethod
    @orm.db_session
    def print_table(time_entries, just_time=False):
        table = {}
        for entry in time_entries:
            k = entry.start.strftime("%Y-%m-%d")
            if k in table:
                table[k] += entry.finish - entry.start
            else:
                table[k] = entry.finish - entry.start
        if table:
            for day, t in table.items():
                ts = t.total_seconds()
                y, m, d = gregorian_to_jalali(*list(map(int, day.split('-'))))
                if not just_time:
                    cprint("{y}-{m:02d}-{d:02d} | {time}".format(y=y, m=m, d=d, time=t), color=Color.get_random_color())
                else:
                    cprint("{0}:{1}:{2}".format(int(ts/3600), int((ts%3600)/60), int((ts%3600)%60)), color=Color.get_random_color())

        else:
            print('No entry found...')
