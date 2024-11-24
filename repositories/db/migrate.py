import os

from alembic.config import Config
from alembic import command
from alembic import op
from misc.config import *

def alembic_auto_migrate():
    # set the paths values
    from os.path import dirname as up
    root_directory = up(up(os.path.dirname(os.path.abspath(__file__))))
    alembic_directory = os.path.join(root_directory, 'alembic')
    ini_path = os.path.join(root_directory, 'alembic.ini')

    # create Alembic config and feed it with paths
    config = Config(ini_path)
    config.set_main_option('script_location', alembic_directory)

    config.set_main_option("sqlalchemy.url", f"postgresql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}")
    # prepare and run the command
    revision = 'head'
    sql = False
    tag = None

    # upgrade command
    command.upgrade(config, revision, sql=sql, tag=tag)