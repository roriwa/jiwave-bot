#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import functools
import discord
from discord.ext import commands
from database import Session, dbm
from . import _util  # noqa


async def setup(bot: commands.Bot):
    bot.event(
        functools.wraps(on_reaction_add)(
            functools.partial(
                on_reaction_add,
                bot
            )
        )
    )


async def on_reaction_add(bot: commands.Bot, reaction: discord.Reaction, _: discord.User):

    config = getArchiveConfig(reaction)

    if not config:
        return

    emojis = _util.string2emojis(config.emoticon)
    reactions = reaction.message.reactions

    if sum(r.count for r in reactions if str(r) in emojis) < config.count:
        return

    archived = alreadyArchived(reaction.message)
    if archived:
        return

    archive = bot.get_channel(config.target_id)
    embed = buildEmbed(message=reaction.message)
    archive_message = await archive.send(embed=embed)
    archiveRegister(reaction.message, archive_message)


def getArchiveConfig(reaction: discord.Reaction) -> dbm.ArchiveConfig:
    guild = reaction.message.guild
    channel = reaction.message.channel

    with Session() as session:
        return session\
            .query(dbm.ArchiveConfig)\
            .filter(
                dbm.ArchiveConfig.guild_id == guild.id,
                dbm.ArchiveConfig.source_id == channel.id,
                dbm.ArchiveConfig.emoticon.contains(str(reaction))
            )\
            .one_or_none()


def archiveRegister(message: discord.Message, archived: discord.Message):
    archived = dbm.ArchiveMessage(
        message_id=message.id,
        archive_id=archived.id
    )

    with Session() as session:
        session.add(archived)
        session.commit()


def alreadyArchived(message: discord.Message) -> dbm.ArchiveMessage:
    with Session() as session:
        return session\
            .query(dbm.ArchiveMessage)\
            .filter(dbm.ArchiveMessage.message_id == message.id)\
            .one_or_none()


def buildEmbed(message: discord.Message) -> discord.Embed:
    author = message.author

    embed = discord.Embed(
        title="see message",
        url=message.jump_url,
        color=discord.Colour.dark_gold()
    )
    embed.set_author(
        name=author.name,
        icon_url=author.avatar.url if author.avatar else author.default_avatar.url
    )
    embed.description = message.content
    image, attachments = getImageAndAttachments(message.attachments)
    if image:
        embed.set_image(url=image.url)
    for attachment in attachments:
        embed.add_field(
            name="Attachment",
            value=f"[{attachment.filename}]({attachment.url})",
            inline=False
        )
    embed.timestamp = message.created_at

    return embed


def getImageAndAttachments(attachments: [discord.Attachment])\
        -> t.Tuple[t.Optional[discord.Attachment], t.List[discord.Attachment]]:
    r"""
    function filter the first image out
    """
    for index, attachment in enumerate(attachments):
        if attachment.content_type and attachment.content_type.startswith('image/'):
            return attachment, (attachments[:index] + attachments[index+1:])
    return None, attachments
