#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import asyncio
import logging
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
                    channelEdit(channel=channel, name=timestring)
                )

    await asyncio.gather(*all_edits)


async def channelEdit(channel: discord.VoiceChannel, name: str):
    try:
        await channel.edit(reason="time-update", name=name)
    except Exception as exception:
        datamanagement.createLogRecord(
            guild=channel.guild,
            message=f"{channel.name}:{exception.__class__.__name__}:{exception}"
        )
        raise exception


@channelUpdater.before_loop
async def waitForReady():
    from main import bot
    await bot.wait_until_ready()


@channelUpdater.error
async def onError(exception: Exception):
    logging.error(str(exception), exc_info=exception)


def getTimeText(template: str, target: datetime):
    # datestr = timeStringHumanized(target)  # '2 days, 1 hour and 33.12 seconds'
    datestr = timeStringDays(target)  # '5 days'
    return template.format(
        time=datestr
    )


def timeStringHumanized(target: datetime):
    now = dateutils.today()
    delta = now - target
    return humanize.precisedelta(delta, minimum_unit='hours')


def timeStringDays(target: datetime):
    now = dateutils.today()
    delta = now - target
    days = delta.days
    return f"{days} {'day' if days == 1 else 'days'}"
