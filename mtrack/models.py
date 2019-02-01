from datetime import datetime

from pony import orm

from mtrack.database import db
from mtrack.utils import GetOrCreateMixin, now


class Project(db.Entity, GetOrCreateMixin):
    name = orm.Required(str)
    time_intervals = orm.Set('TimeEntry')

    @classmethod
    @orm.db_session
    def get_or_create_project(cls, project_name):
        project, created = cls.get_or_create(name=project_name)
        if created:
            print(f'Created project {project_name}')
        return project


class TimeEntry(db.Entity):
    project = orm.Required(Project)
    start = orm.Required(datetime)
    finish = orm.Optional(datetime)

    @classmethod
    @orm.db_session
    def start_timer(cls, project_id):
        return cls(project=project_id, start=now())

    @classmethod
    @orm.db_session
    def stop_timer(cls, interval_id, dt):
        interval = cls[interval_id]
        interval.finish = dt
        return interval
