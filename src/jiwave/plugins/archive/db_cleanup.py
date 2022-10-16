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
    databaseCleanup.start()


@tasks.loop(hours=6)
@utility.logCalling
async def databaseCleanup():
    expiration_days = 7
    with Session() as session:
        limit = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
        session.query(dbm.ArchiveMessage).filter(dbm.ArchiveMessage.timestamp <= limit).delete()
        session.commit()


@databaseCleanup.error
async def onError(exception: Exception):
    logging.error(str(exception), exc_info=exception)
