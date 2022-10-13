#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import logging
from discord.ext import tasks
import database
import utility


async def setup(_):
    reduceLogs.start()


@tasks.loop(hours=6)
@utility.logCalling
async def reduceLogs():
    database.reduceLogs()


@reduceLogs.error
async def onError(exception: Exception):
    logging.error(str(exception), exc_info=exception)
