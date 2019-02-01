from datetime import datetime

from pony import orm

from mtrack.database import db
from mtrack.utils import GetOrCreateMixin


class Project(db.Entity, GetOrCreateMixin):
    name = orm.Required(str)
    time_intervals = orm.Set('TimeInterval')


class TimeInterval(db.Entity):
    project = orm.Required(Project)
    start = orm.Required(datetime)
    finish = orm.Optional(datetime)
