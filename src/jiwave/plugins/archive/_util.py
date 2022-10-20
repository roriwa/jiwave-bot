#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import discord
from discord.ext import commands


Emoji = t.Union[discord.PartialEmoji, discord.Emoji, str]


def emojis2string(emojis: t.List[Emoji]) -> str:
    return ';'.join(str(e) for e in emojis)


def string2emojis(text: str, bot: commands.Bot = None) -> t.List[str]:
    if not bot:
        return [x for x in text.split(';')]
    else:
        emojis = []
        for emoji in text.split(';'):
            try:
                emoji_id = int(emoji)
                emojis.append(bot.get_emoji(emoji_id))
            except ValueError:
                emojis.append(emoji)

        return emojis
