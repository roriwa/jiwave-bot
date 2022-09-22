#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import discord
from discord.ext import commands


async def setup(bot: commands.Bot):
    bot.remove_command(cmd_help.name)
    bot.add_command(cmd_help)


@commands.command(name="help")
async def cmd_help(context: commands.Context, *, commandName: str = None):
    r"""
    gives information about the bot and his commands
    """
    embed = discord.Embed(title=f"Help for {commandName if commandName else 'jiwave-bot'}")
    if commandName:
        command = context.bot.get_command(commandName)
        if not command:
            embed.colour = discord.Colour.red()
            embed.description = f"command {commandName} not found"
        else:
            embed.colour = discord.Colour.green()
            embed.add_field(name=f"{command.name} {command.signature}", value=command.description, inline=False)
    else:
        usable_commands = await getAvailableCommands(context)
        if usable_commands:
            for command in usable_commands:

                embed.add_field(name=command.qualified_name, value=getCommandHelp(command))
        else:
            embed.description = "no commands found"

    await context.reply(embed=embed)


cmd_help: commands.Command


def getCommandHelp(command: commands.Command):
    for attr in ['help', 'description', 'brief']:
        if hasattr(command, attr):
            return getattr(command, attr)
    return "no help available"


async def getAvailableCommands(context: commands.Context):
    bot = context.bot
    usable = []
    for command in bot.commands:
        try:
            if not command.hidden and await command.can_run(context):
                usable.append(command)
        except Exception:  # noqa
            pass
    return usable
