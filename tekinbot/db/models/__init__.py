import importlib

from sqlalchemy.ext.declarative import declarative_base

__all__ = [
    'karma',
]

tables = {}

TekinTableBase = declarative_base()

for module in __all__:
    tables[module] = importlib.import_module(f'tekinbot.db.models.{module}')
