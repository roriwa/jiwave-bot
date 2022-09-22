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


@tasks.loop(minutes=5)  # update every hour, maybe every day later
@utility.logCalling
async def channelUpdater():
    from main import bot

    all_edits = []

    for guild in bot.guilds:
        configs = datamanagement.listChannels(guild=guild)

        if not configs:
            datamanagement.createLogRecord(
                guild=guild,
                message=f"no channels configured for this guild"
            )
            continue

        guild_config = datamanagement.getGuildConfig(guild=guild)
        template = guild_config.message_template
        for config in configs:
            channel: discord.VoiceChannel = bot.get_channel(config.channel_id)
            if not channel:
                datamanagement.createLogRecord(
                    guild=guild,
                    message=f"channel not found. can't update. ({config.guild_id}: {config.channel_orig_name})"
                )
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
    # datestr = timeStringHumanized(target)  # '1 month, 7 days and 1 hour'
    datestr = timeStringDays(target)  # '5 days'
    return template.format(
        time=datestr
    )


def timeStringHumanized(target: datetime):
    now = dateutils.today()
    delta = now - target
    return humanize.precisedelta(delta, minimum_unit='hours')
    # '1 month, 7 days and 1 hour'


def timeStringDays(target: datetime):
    now = dateutils.today()
    delta = target - now
    days = delta.days
    if days <= 0:
        return "no days"
    return f"{days} {'day' if days == 1 else 'days'}"
    # '184 days'
