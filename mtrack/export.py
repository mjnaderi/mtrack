from datetime import datetime, timedelta
from pony import orm

from mtrack.database import init_db
from mtrack.jalali import jalali_to_gregorian, gregorian_to_jalali
from mtrack.models import Project, TimeEntry
from mtrack.color_print import Color, cprint


def export(project_name, date):
    init_db()
    hours_table(project_name, date)
    work_done = calculate_workdone(project_name, date)
    print("{}:{}".format(work_done.days * 24 + work_done.seconds // 3600, (work_done.seconds // 60) % 60))


@orm.db_session
def get_time_entries(project_name, date):
    jy, jm, jd = list(map(int, date.split('-'))) + [1]
    start_date = datetime(*jalali_to_gregorian(jy, jm, jd))
    jm += 1
    if jm == 13:
        jm = 1 
        jy += 1
    finish_date = datetime(*jalali_to_gregorian(jy, jm, jd))
    project = Project.get(name=project_name)
    time_entries = TimeEntry.select(
        lambda t: t.start >= start_date and t.start <= finish_date and t.project == project) \
        .order_by(lambda t: t.start)
    return time_entries


@orm.db_session
def calculate_workdone(project_name, date):
    time_entries = get_time_entries(project_name, date)
    return sum([time_entry.finish - time_entry.start for time_entry in time_entries], timedelta())


@orm.db_session
def hours_table(project_name, date):
    time_entries = get_time_entries(project_name, date)
    table = {}
    for e in time_entries:
        if e.start.strftime("%Y-%m-%d") in table:
            table[e.start.strftime("%Y-%m-%d")] += e.finish - e.start
        else:
            table[e.start.strftime("%Y-%m-%d")] = e.finish - e.start
    for day in table:
        gy, gm, gd = list(map(int, day.split('-')))
        jalali_day = datetime(*gregorian_to_jalali(gy, gm, gd))
        cprint("{day} | {total_hours}".format(day=jalali_day.strftime('%Y-%m-%d'), total_hours=table[day]),
               color=Color.get_random_color())
