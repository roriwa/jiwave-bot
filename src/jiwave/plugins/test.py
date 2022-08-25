#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from discord.ext import commands


async def setup(bot: commands.Bot):
    bot.add_command(cmd_test)


@commands.command(name="test")
@commands.is_owner()
async def cmd_test(context: commands.Context):
    await context.reply("coming soon...")


cmd_test: commands.Command
