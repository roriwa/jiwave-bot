#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import logging
from discord.ext import tasks
import datamanagement
import utility


async def setup(_):
    reduceLogs.start()


@tasks.loop(hours=6)
@utility.logCalling
async def reduceLogs():
    datamanagement.reduceLogs()


@reduceLogs.error
async def onError(exception: Exception):
    logging.error(str(exception), exc_info=exception)