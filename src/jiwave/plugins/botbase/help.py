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
        if not command or not await canBeUsed(context, command):
            embed.colour = discord.Colour.red()
            embed.description = f"command {commandName} not found"
        else:
            embed.colour = discord.Colour.green()
            embed.add_field(
                name=f"{context.clean_prefix}{command.name} {command.signature}",
                value=getCommandHelp(command),
                inline=False
            )
            if isinstance(command, commands.Group):
                usable_commands = await getAvailableCommands(context, command.commands)
                for subcommand in usable_commands:
                    embed.add_field(
                        name=f"{context.clean_prefix}{subcommand} {subcommand.signature}",
                        value=getCommandHelp(subcommand),
                        inline=False
                    )
    else:
        usable_commands = await getAvailableCommands(context, context.bot.commands)
        if usable_commands:
            for command in usable_commands:
                embed.add_field(name=command.qualified_name, value=getCommandHelp(command))
        else:
            embed.description = "no commands found"

    await context.reply(embed=embed)


cmd_help: commands.Command


def getCommandHelp(command: commands.Command):
    for attr in ['brief', 'description', 'help']:
        if getattr(command, attr, None):
            return getattr(command, attr).split('\n', 1)[0]
    return "no help available"


async def getAvailableCommands(context: commands.Context, command_list: [commands.Command]):
    usable = []
    for command in command_list:
        if await canBeUsed(context, command):
            usable.append(command)
    usable.sort(key=lambda cmd: cmd.name)
    return usable


async def canBeUsed(context: commands.Context, command: commands.Command | commands.GroupMixin) -> bool:
    if command.hidden:
        return False
    if command.parent and not await canBeUsed(context, command.parent):
        return False
    try:
        if await command.can_run(context):
            return True
    except Exception:  # noqa
        return False
    else:
        return False
