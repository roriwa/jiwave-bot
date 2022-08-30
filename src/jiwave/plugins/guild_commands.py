#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import discord
from discord.ext import commands
import datamanagement


async def setup(bot: commands.Bot):
    bot.add_command(cmd_timeformat)


@commands.command(name="timeformat", aliases=['format', 'template'])
async def cmd_timeformat(context: commands.Context, *, template: str = None):
    if template is None:
        pass
    elif template in ['default', 'reset']:
        datamanagement.setTimeFormat(guild=context.guild, message_template="{time}")
    else:
        if not verifyTemplate(template):
            raise ValueError("invalid template. template must contain '{time}'")

        datamanagement.setTimeFormat(guild=context.guild, message_template=template)

    config = datamanagement.getGuildConfig(guild=context.guild)

    embed = discord.Embed(
        color=discord.Color.green(),
        title="Timeformat for this Server",
        description=f"{config.message_template}"
    )
    await context.reply(embed=embed)


def verifyTemplate(template: str) -> bool:
    try:
        # one dry formatting
        template.format(
            time="01.01.1970"
        )
        return "{time}" in template  # verify that the time is at least once used
    except KeyError:
        return False


cmd_timeformat: commands.Command