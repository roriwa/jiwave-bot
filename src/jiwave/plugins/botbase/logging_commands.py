#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import discord
from discord.ext import commands
from database import Session, dbm


async def setup(bot: commands.Bot):
    bot.add_command(cmd_logs)


@commands.command(name="logs")
@commands.guild_only()
@commands.has_guild_permissions(manage_guild=True)
async def cmd_logs(context: commands.Context):
    r"""
    show problems and notifications from the bot
    """
    with Session() as session:
        last_logs: [dbm.LogRecord] = session\
            .query(dbm.LogRecord)\
            .filter(dbm.LogRecord.guild_id == context.guild.id)\
            .order_by(dbm.LogRecord.timestamp.desc())\
            .limit(25)\
            .all()

    if not last_logs:
        embed = discord.Embed(
            title="No logs found",
            color=discord.Color.orange()
        )
    else:
        embed = discord.Embed(
            color=discord.Color.green()
        )
        for log in last_logs:
            embed.add_field(
                name=log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                value=f"```txt\n{log.message}```",
                inline=False
            )

    await context.reply(embed=embed)


cmd_logs: commands.Command
