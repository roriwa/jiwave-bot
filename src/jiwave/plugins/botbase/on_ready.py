#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import asyncio
import functools
from datetime import datetime
import discord
from discord.ext import commands
import utility


async def setup(bot: commands.Bot):
    bot.event(
        functools.wraps(on_ready)(
            functools.partial(
                on_ready,
                bot
            )
        )
    )


# @main.bot.event
@utility.logCalling
async def on_ready(bot: commands.Bot):
    await setStatusMessage(bot, f"just started ({datetime.now().isoformat(sep=' ', timespec='seconds')})")
    await asyncio.sleep(30)
    await setStatusMessage(bot, "about this Server")


async def setStatusMessage(bot: commands.Bot, text: str):
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=text,
        ),
        status=discord.Status.online
    )