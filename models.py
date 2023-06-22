from datetime import datetime

from peewee import (AutoField, BooleanField, CharField, DateTimeField, Model,
                    SqliteDatabase)

db = SqliteDatabase(None)


class Clock(Model):
    clock_id = AutoField()
    at = DateTimeField(default=datetime.now)
    ip_addr = CharField(default="")
    session_begin = BooleanField(default=False)

    _db_inited: bool = False

    class Meta:
        table_name = "clocks"
        database = db

    @classmethod
    def setup_database(cls, db_path: str) -> bool:
        """Setup database before any usage"""
        if cls._db_inited:
            return False
        db.init(db_path)
        cls._db_inited = True
        cls.settle_table()
        return True

    @classmethod
    def settle_table(cls):
        """Simple table creation, not account for migration"""
        if not cls.table_exists():
            cls.create_table()
