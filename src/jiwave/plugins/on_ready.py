#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import asyncio

import discord
from discord.ext import commands
import utility
from datetime import datetime


async def setup(bot: commands.Bot):
    bot.event(on_ready)


# @main.bot.event
@utility.logCalling
async def on_ready():
    await setStatusMessage(f"just started ({datetime.now().isoformat(sep=' ', timespec='seconds')})")
    await asyncio.sleep(30)
    await setStatusMessage("about this Server")


async def setStatusMessage(text: str):
    import main
    await main.bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=text,
        ),
        status=discord.Status.online
    )