import sqlalchemy as sql
import sqlite3


class Database(object):
    def __init__(self):
        self.db_engine = sql.create_engine("sqlite:////home/chris/.databases/music_master.db")


    def build_tables(self):
