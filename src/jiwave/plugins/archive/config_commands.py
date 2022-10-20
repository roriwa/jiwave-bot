#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import discord
from discord.ext import commands
from database import Session, dbm
from . import util  # noqa


async def setup(bot: commands.Bot):
    bot.add_command(cmd_archive)


@commands.group('archive')
async def cmd_archive(_: commands.Context):
    pass


cmd_archive: commands.Group


@cmd_archive.command(name="list")
async def cmd_list(context: commands.Context):
    r"""
    list all for this server configured channels
    """
    embed = discord.Embed(title="Configured Channels")
    embed.colour = discord.Color.green()

    with Session() as session:
        configs: [dbm.ArchiveConfig] = session\
            .query(dbm.ArchiveConfig)\
            .filter(dbm.ArchiveConfig.guild_id == context.guild.id)\
            .all()

    if not configs:
        embed.description = "No configured channels"
    else:
        for config in configs:
            source: discord.TextChannel = context.bot.get_channel(config.channel_id)
            target: discord.TextChannel = context.bot.get_channel(config.channel_id)
            embed.add_field(
                name=f"{getattr(source, 'name', '~404~')} -> {getattr(target, 'name', '~404~')}",
                value=f"{config.count} of {', '.join(e for e in util.string2emojis(config.emoticon))}",
                inline=False)

    await context.reply(embed=embed)


@cmd_archive.command(name="info", aliases=['get'])
async def cmd_info(context: commands.Context, channel: discord.TextChannel):
    r"""
    get the time for a channel
    """
    with Session() as session:
        config: dbm.ArchiveConfig = session\
            .query(dbm.ArchiveConfig)\
            .filter(dbm.ArchiveConfig.guild_id == context.guild.id, dbm.ArchiveConfig.source_id == channel.id)\
            .one_or_none()

    embed = discord.Embed(color=discord.Color.green())

    if config:
        archive = context.bot.get_channel(config.target_id)
        embed.title = f"Configured for {getattr(archive, 'name', '~404~')}" \
                      f"with {', '.join(e for e in util.string2emojis(config.emoticon))}"
    else:
        embed.title = "Channel is not Configured"

    await context.reply(embed=embed)


@cmd_archive.command(name="add", aliases=['set'])
async def cmd_add(context: commands.Context, source: discord.TextChannel, target: discord.TextChannel, count: int,
                  emojis: commands.Greedy[discord.Emoji]):
    r"""
    add or update the time for a channel
    """
    with Session() as session:
        obj: dbm.ArchiveConfig = session\
            .query(dbm.ArchiveConfig)\
            .filter(dbm.ArchiveConfig.guild_id == context.guild.id,
                    dbm.ArchiveConfig.source_id == source.id,
                    dbm.ArchiveConfig.target_id == target.id)\
            .one_or_none()

        if obj:
            obj.count = count
            obj.emoticon = util.emojis2string(emojis)
        else:
            config = dbm.ArchiveConfig(
                guild_id=context.guild.id,
                source_id=source.id,
                target_id=target.id,
                emoticon=util.emojis2string(emojis),
                count=count,
            )
            session.add(config)

        session.commit()

    embed = discord.Embed(
        color=discord.Color.green(),
        title=f"{source.name} -> {target.name} was added",
        description=f"{source.name} archives to {target.name}"
                    f"after {count} reactions of {', '.join(str(e) for e in emojis)}"
    )
    await context.reply(embed=embed)


@cmd_archive.command(name="ignore", aliases=['remove'])
async def cmd_ignore(context: commands.Context, channel: discord.TextChannel):
    r"""
    remove a channel
    """
    with Session() as session:
        session.query(dbm.ArchiveConfig)\
            .filter(dbm.ArchiveConfig.guild_id == context.guild.id, dbm.ArchiveConfig.source_id == channel.id)\
            .delete()

    embed = discord.Embed(
        color=discord.Color.green(),
        title=f"{channel.name} is now ignored"
    )
    await context.reply(embed=embed)


cmd_list: commands.Command
cmd_info: commands.Command
cmd_add: commands.Command
cmd_ignore: commands.Command
