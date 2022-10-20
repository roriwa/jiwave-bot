#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import logging
import datetime
from discord.ext import tasks
from database import Session, dbm
import utility


async def setup(_):
    databaseLogCleanup.start()


@tasks.loop(hours=6)
@utility.logCalling
async def databaseLogCleanup():
    expiration_days = 14
    with Session() as session:
        limit = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
        session.query(dbm.LogRecord).filter(dbm.LogRecord.timestamp <= limit).delete()
        session.commit()


@databaseLogCleanup.error
async def onError(exception: Exception):
    logging.error(str(exception), exc_info=exception)
