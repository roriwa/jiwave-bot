#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import asyncio
import dateutil.parser as dateparser
import discord
from discord.ext import commands
from database import Session, dbm
from channel_updater import guildUpdate


async def setup(bot: commands.Bot):
    bot.add_command(cmd_timer)


@commands.group('timer')
@commands.guild_only()
@commands.has_guild_permissions(manage_guild=True)
async def cmd_timer(_: commands.Context):
    pass


cmd_timer: commands.Group


@cmd_timer.command(name="list")
async def cmd_list(context: commands.Context):
    r"""
    list all for this server configured channels
    """
    embed = discord.Embed(title="Configured Channels")
    embed.colour = discord.Color.green()

    guild = context.guild

    with Session() as session:
        configured_channels: [dbm.TimerConfig] = session\
            .query(dbm.TimerConfig)\
            .filter(dbm.TimerConfig.guild_id == guild.id)\
            .all()

    if not configured_channels:
        embed.description = "No configured channels"
    else:
        for config in configured_channels:
            channel: discord.VoiceChannel = context.bot.get_channel(config.channel_id)
            embed.add_field(
                name=channel.name,
                value=config.target_time.strftime("%d.%m.%Y"),
                inline=False)

    await context.reply(embed=embed)


@cmd_timer.command(name="info", aliases=['get'])
async def cmd_info(context: commands.Context, channel: discord.VoiceChannel):
    r"""
    get the time for a channel
    """

    with Session() as session:
        config = session\
            .query(dbm.TimerConfig)\
            .filter(dbm.TimerConfig.guild_id == context.guild.id, dbm.TimerConfig.channel_id == channel.id)\
            .one_or_none()

    embed = discord.Embed(color=discord.Color.green())

    if config:
        embed.title = f"Configured for {config.target_time.strftime('%d.%m.%Y')}"
    else:
        embed.title = "Channel is not Configured"

    await context.reply(embed=embed)


@cmd_timer.command(name="add", aliases=['set'])
async def cmd_add(context: commands.Context, channel: discord.VoiceChannel, date: str):
    r"""
    add or update the time for a channel
    """
    date = dateparser.parse(date, dayfirst=True)
    channel_name = channel.name

    timer_config = dbm.TimerConfig(
        guild_id=context.guild.id,
        channel_id=channel.id,
        channel_orig_name=channel_name,
        target_time=date
    )

    with Session() as session:
        session.merge(timer_config)

    embed = discord.Embed(
        color=discord.Color.green(),
        title=f"{channel_name} was added",
        description=f"target date was recognised as {date.strftime('%d.%m.%Y')}"
    )
    await context.reply(embed=embed)

    asyncio.create_task(guildUpdate(bot=context.bot, guild=context.guild))


@cmd_timer.command(name="ignore", aliases=['remove'])
async def cmd_ignore(context: commands.Context, channel: discord.VoiceChannel):
    r"""
    remove a channel
    """
    with Session() as session:
        q = session\
            .query(dbm.TimerConfig)\
            .filter(dbm.TimerConfig.guild_id == context.guild.id, dbm.TimerConfig.channel_id == channel.id)

        config: dbm.TimerConfig = q.one()
        q.delete()

    await channel.edit(reason="channel will no longer be updated", name=config.channel_orig_name)
    embed = discord.Embed(
        color=discord.Color.green(),
        title=f"{config.channel_orig_name} is no longer updated"
    )
    await context.reply(embed=embed)


cmd_list: commands.Command
cmd_info: commands.Command
cmd_add: commands.Command
cmd_ignore: commands.Command


@cmd_timer.command(name="format", aliases=['format', 'template'])
async def cmd_format(context: commands.Context, *, template: str = None):
    r"""
    set the time-format for this server

    {time} left => 185 days left
    """

    if template is None:
        pass  # just do nothing (equal to only read the current timeformat)
    elif template in ['default', 'reset']:
        with Session() as session:
            session.query()\
                .filter(dbm.GuildConfig.guild_id == context.guild.id)\
                .delete()
    else:
        if not verifyTemplate(template):
            raise ValueError("invalid template. template must contain '{time}'")

        with Session() as s:
            tmc: dbm.GuildConfig = s\
                .query(dbm.GuildConfig)\
                .filter(dbm.GuildConfig.guild_id == context.guild.id)\
                .one()
            tmc.message_template = template
            s.commit()

        asyncio.create_task(guildUpdate(bot=context.bot, guild=context.guild))

    with Session() as session:
        config: dbm.GuildConfig = session\
            .query(dbm.GuildConfig)\
            .filter(dbm.GuildConfig.guild_id == context.guild.id)\
            .one_or_none()

    embed = discord.Embed(
        color=discord.Color.green(),
        title="Timeformat for this Server",
        description=f"{config.message_template if config else '{time}'}"
    )
    await context.reply(embed=embed)


def verifyTemplate(template: str) -> bool:
    try:
        # one dry formatting
        template.format(
            time="365 days"
        )
        return "{time}" in template  # verify that the time is at least once used
    except KeyError:
        return False


cmd_format: commands.Command
