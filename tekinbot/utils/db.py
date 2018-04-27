import functools

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import tekinbot.db.models  # noqa
from tekinbot.db.models import TekinTableBase
from tekinbot.utils.config import tekin_secrets
# we need to import tekinbot.db.models so that
# sqlalchemy knows where to find all the table
# models


TEKIN_DB_UN = tekin_secrets('database.username')
TEKIN_DB_PW = tekin_secrets('database.password')
DB_NAME = 'tekinbot'
in_memory = False


@functools.lru_cache(maxsize=1)
def get_engine():
    return create_engine(
        f'mysql+mysqlconnector://'
        f'{TEKIN_DB_UN}:{TEKIN_DB_PW}@localhost/'
        f'{DB_NAME}'
    )


@functools.lru_cache(maxsize=1)
def get_memory_engine():
    return create_engine(
        'sqlite://'
    )


@functools.lru_cache(maxsize=1)
def session_maker():
    return sessionmaker(bind=(
        get_memory_engine() if in_memory else get_engine()
    ))


def get_session():
    return session_maker()()


def tekin_db_init(nodb=False):
    global in_memory
    if nodb:
        in_memory = True
        engine = get_memory_engine()
    else:
        engine = get_engine()
    TekinTableBase.metadata.create_all(engine, checkfirst=True)
    print('tekin database initialized')
