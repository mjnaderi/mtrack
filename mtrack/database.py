import logging
import os
from importlib import import_module

from pony import orm

db = orm.Database()


def init_db():
    data_dir = os.path.expanduser('~/.mtrack')
    if not os.path.exists(data_dir):
        logging.info('Data directory not found. Creating %s', data_dir)
        os.mkdir(data_dir)
    db_file = os.path.join(data_dir, 'db.sqlite')

    logging.info('init database')
    import_module('mtrack.models')  # Discover models
    db.bind(provider='sqlite', filename=db_file, create_db=True)
    db.generate_mapping(create_tables=True)
