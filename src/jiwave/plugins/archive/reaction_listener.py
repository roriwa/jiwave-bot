#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import functools
import discord
from discord.ext import commands
from database import Session, dbm


def setup(bot: commands.Bot):
    bot.event(
        functools.partial(
            on_reaction_add,
            bot
        )
    )


async def on_reaction_add(bot: commands.Bot, reaction: discord.Reaction, _: discord.User):
    guild = reaction.message.guild
    channel = reaction.message.channel

    with Session() as session:
        config: dbm.ArchiveConfig = session\
            .query(dbm.ArchiveConfig)\
            .filter(
                dbm.ArchiveConfig.guild_id == guild.id,
                dbm.ArchiveConfig.source_id == channel.id,
                dbm.ArchiveConfig.emoticon == str(reaction)
            )\
            .one_or_none()

    if config:
        if reaction.count >= config.count:
            archive = bot.get_channel(config.target_id)
