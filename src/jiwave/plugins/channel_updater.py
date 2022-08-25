#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import traceback
from datetime import datetime

import discord
from discord.ext import tasks
import dateutil.utils as dateutils
import humanize
import datamanagement


async def setup(_):
    channelUpdater.start()


@tasks.loop(hours=1)  # update every hour, maybe every day later
async def channelUpdater():
    from main import bot

    for guild in bot.guilds:
        configs = datamanagement.listChannels(guild=guild)
        for config in configs:
            channel: discord.VoiceChannel = bot.get_channel(config.channel_id)
            timestring = getTimeText(target=config.target_time)
            if channel.name != timestring:
                await channel.edit(reason="time-update", name=timestring)


@channelUpdater.before_loop
async def waitForReady():
    from main import bot
    await bot.wait_until_ready()


@channelUpdater.error
async def onError(exception: Exception):
    traceback.print_exception(type(exception), exception, exception.__traceback__)


def getTimeText(target: datetime):
    now = dateutils.today()
    delta = now - target
    return humanize.precisedelta(delta, minimum_unit='hours')
