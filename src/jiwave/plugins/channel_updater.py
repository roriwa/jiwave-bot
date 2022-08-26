#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import asyncio
import logging
import traceback
from datetime import datetime

import discord
from discord.ext import tasks
import dateutil.utils as dateutils
import humanize
import datamanagement
import utility


async def setup(_):
    channelUpdater.start()


@tasks.loop(hours=1)  # update every hour, maybe every day later
@utility.logCalling
async def channelUpdater():
    from main import bot

    all_edits = []

    for guild in bot.guilds:
        configs = datamanagement.listChannels(guild=guild)
        guild_config = datamanagement.getGuildConfig(guild=guild)
        template = guild_config.message_template
        for config in configs:
            channel: discord.VoiceChannel = bot.get_channel(config.channel_id)
            if not channel:
                logging.warning(f"channel not found. can't update. ({config.guild_id}: {config.channel_orig_name})")
                continue

            timestring = getTimeText(template=template, target=config.target_time)
            if channel.name != timestring:
                all_edits.append(
                    channel.edit(reason="time-update", name=timestring)
                )

    await asyncio.gather(*all_edits)


@channelUpdater.before_loop
async def waitForReady():
    from main import bot
    await bot.wait_until_ready()


@channelUpdater.error
async def onError(exception: Exception):
    traceback.print_exception(type(exception), exception, exception.__traceback__)


def getTimeText(template: str, target: datetime):
    now = dateutils.today()
    delta = now - target
    datestr = humanize.precisedelta(delta, minimum_unit='hours')
    return template.format(
        time=datestr
    )
