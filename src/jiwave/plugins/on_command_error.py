#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import re
import discord
from discord.ext import commands
import utility


@utility.logCalling
async def setup(bot: commands.Bot):
    bot.event(on_command_error)


async def on_command_error(context: commands.Context, error: Exception):
    embed = discord.Embed(
        color=discord.Color.red(),
        title=formatClassName(error.__class__.__qualname__),
        description=str(error))
    await context.reply(embed=embed)


def formatClassName(className: str) -> str:
    # basically only add space before uppercase letters
    return re.sub('[A-Z]', lambda c: f" {c.group()}", className).strip()
