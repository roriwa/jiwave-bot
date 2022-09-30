#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import discord
from discord.ext import commands
import datamanagement


def setup(bot: commands.Bot):
    bot.event(on_reaction_add)


async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    channel = reaction.message.channel
