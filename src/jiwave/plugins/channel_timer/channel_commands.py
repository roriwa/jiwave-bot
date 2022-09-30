#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import dateutil.parser as dateparser
import discord
from discord.ext import commands
import datamanagement


async def setup(bot: commands.Bot):
    bot.add_command(cmd_list)
    bot.add_command(cmd_info)
    bot.add_command(cmd_add)
    bot.add_command(cmd_ignore)

    bot.add_command(cmd_timeformat)


@commands.command(name="list")
@commands.guild_only()
@commands.has_guild_permissions(manage_guild=True)
async def cmd_list(context: commands.Context):
    r"""
    list all for this server configured channels
    """
    embed = discord.Embed(title="Configured Channels")
    embed.colour = discord.Color.green()

    guild = context.guild

    configured_channels = datamanagement.listChannels(guild=guild)

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


@commands.command(name="info", aliases=['get'])
@commands.guild_only()
@commands.has_guild_permissions(manage_guild=True)
async def cmd_info(context: commands.Context, channel: discord.VoiceChannel):
    r"""
    get the time for a channel
    """
    config = datamanagement.getChannelConfig(guild=context.guild, channel=channel)
    embed = discord.Embed(color=discord.Color.green())

    if config:
        embed.title = f"Configured for {config.target_time.strftime('%d.%m.%Y')}"
    else:
        embed.title = "Channel is not Configured"

    await context.reply(embed=embed)


@commands.command(name="add", aliases=['set'])
@commands.guild_only()
@commands.has_guild_permissions(manage_guild=True)
async def cmd_add(context: commands.Context, channel: discord.VoiceChannel, date: str):
    r"""
    add or update the time for a channel
    """
    date = dateparser.parse(date, dayfirst=True)
    channel_name = channel.name
    datamanagement.addOrUpdateChannel(guild=context.guild, channel=channel, date=date)
    embed = discord.Embed(
        color=discord.Color.green(),
        title=f"{channel_name} was added",
        description=f"target date was recognised as {date.strftime('%d.%m.%Y')}"
    )
    await context.reply(embed=embed)


@commands.command(name="ignore", aliases=['remove'])
@commands.guild_only()
@commands.has_guild_permissions(manage_guild=True)
async def cmd_ignore(context: commands.Context, channel: discord.VoiceChannel):
    r"""
    remove a channel
    """
    config = datamanagement.removeChannel(guild=context.guild, channel=channel)
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


DEFAULT_TIMEFORMAT = "{time}"


@commands.command(name="timeformat", aliases=['format', 'template'])
@commands.guild_only()
@commands.has_guild_permissions(manage_guild=True)
async def cmd_timeformat(context: commands.Context, *, template: str = None):
    r"""
    set the timeformat for this server

    {time} left => 185 days left
    """

    if template is None:
        pass  # just do nothing (equal to only read the current timeformat)
    elif template in ['default', 'reset']:
        datamanagement.setTimeFormat(guild=context.guild, message_template=DEFAULT_TIMEFORMAT)
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
