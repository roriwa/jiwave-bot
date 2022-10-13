#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import logging
import sqlalchemy as sql
import sqlalchemy.orm
import utility


DATABASE_PATH = utility.localFile('database.sqlite')
logging.info(f"DB-Path: {DATABASE_PATH}")

engine = sql.create_engine(f"sqlite://{DATABASE_PATH}", echo=True)

Base = sql.orm.declarative_base()


def createDatabase():
    Base.metadata.create_all(engine)


class Session(sql.orm.Session):
    def __init__(self, **kwargs):
        super().__init__(binds=engine, **kwargs)

    def __enter__(self) -> sql.orm.Session:
        return super().__enter__()
