#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import asyncio
import logging
import datetime

import discord
from discord.ext import commands
from discord.ext import tasks
import dateutil.utils as dateutils
import humanize
import database
from database import Session, dbm
import utility


async def setup(bot: commands.Bot):
    channelUpdater.start(bot)


# @tasks.loop(minutes=1)
@tasks.loop(hours=1)
@utility.logCalling
async def channelUpdater(bot):
    for guild in bot.guilds:
        await guildUpdate(bot=bot, guild=guild)


@utility.logCalling
async def guildUpdate(bot: commands.Bot, guild: discord.Guild):
    with Session() as session:
        timer_configs: [dbm.TimerConfig] = session\
            .query(dbm.TimerConfig)\
            .filter(dbm.TimerConfig.guild_id == guild.id)\
            .all()

    if not timer_configs:
        return

    with Session() as session:
        guild_config = session\
            .query(dbm.GuildConfig)\
            .filter(dbm.GuildConfig.guild_id == guild.id)\
            .one_or_none()

    template = guild_config.message_template if guild_config else None

    all_edits = []

    for config in timer_configs:
        channel: discord.VoiceChannel = bot.get_channel(config.channel_id)
        if not channel:
            database.createLogRecord(
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
        database.createLogRecord(
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


def getTimeText(template: str, target: datetime.datetime):
    now = dateutils.today()
    delta = target - now
    # datestr = timeStringHumanized(delta)  # '1 month, 7 days and 1 hour'
    datestr = timeStringDays(delta)  # '5 days'
    return (template or "{time}").format(
        time=datestr
    )


def timeStringHumanized(delta: datetime.timedelta):
    return humanize.precisedelta(delta, minimum_unit='hours')
    # '1 month, 7 days and 1 hour'


def timeStringDays(delta: datetime.timedelta):
    days = delta.days
    if days <= 0:
        return "no days"
    return f"{days} {'day' if days == 1 else 'days'}"
    # '184 days'
