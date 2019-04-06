from datetime import datetime, timedelta
from pony import orm

from mtrack.database import init_db
from mtrack.jalali import jalali_to_gregorian
from mtrack.models import Project, TimeEntry


def export(project_name, date):
    init_db()
    print(calculate_hours(project_name, date))


@orm.db_session
def calculate_hours(project_name, date):
    jy, jm, jd = list(map(int, date.split('-'))) + [1]
    start_date = datetime(*jalali_to_gregorian(jy, jm, jd))
    jm += 1
    if jm == 13:
        jm = 0
        jy += 1
    finish_date = datetime(*jalali_to_gregorian(jy, jm, jd))
    project = Project.get(name=project_name)
    time_entries = TimeEntry.select(
        lambda t: t.start >= start_date and t.finish <= finish_date and t.project == project)
    return sum([time_entry.finish - time_entry.start for time_entry in time_entries], timedelta())
