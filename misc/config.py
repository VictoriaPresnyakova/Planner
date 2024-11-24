import os
from distutils.util import strtobool
from os import environ as env

from dotenv import load_dotenv, find_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

SQL_DATABASE = env.get('SQL_DATABASE')
SQL_USER = env.get('SQL_USER')
SQL_PASSWORD = env.get('SQL_PASSWORD')
SQL_HOST = env.get('SQL_HOST')
SQL_PORT = env.get('SQL_PORT')

EMAIL = env.get('EMAIL')
EMAIL_PASSWORD = env.get('EMAIL_PASSWORD')

TEST_MODE = env.get('TEST_MODE') == 'True'





