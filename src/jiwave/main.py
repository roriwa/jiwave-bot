#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import configure_logging  # noqa
import logging
import os
import sys
import discord
from discord.ext import commands
import humanize
from database import base as database_basis
import utility

humanize.i18n.activate('de_DE')


# this line removes a huge bug
# without this line this file is run two times (because of `import main`)
# that's why bot.run is not called and nothing would work
sys.modules['main'] = sys.modules['__main__']


bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    intents=discord.Intents.default()
)


@bot.event
async def on_error(*args):
    logging.error("on-error", exc_info=True)
    logging.error(str(args))


# @setup_hook is not possible, so we use this shortcut
@(lambda c: setattr(bot, c.__name__, c))
@utility.logCalling
async def setup_hook():
    try:
        for plugin in os.listdir('plugins'):
            if plugin.startswith('_'):
                continue

            if os.path.isdir(os.path.join("plugins", plugin)):
                group = plugin
                for module in os.listdir(os.path.join('plugins', group)):
                    if module.startswith('_'):
                        continue
                    module = os.path.splitext(module)[0]
                    name = f'plugins.{group}.{module}'
                    logging.debug(f"Load Plugin: {name!r}")
                    await bot.load_extension(name)
            else:
                plugin = os.path.splitext(plugin)[0]
                name = f'plugins.{plugin}'
                logging.debug(f"Load Plugin: {name!r}")
                await bot.load_extension(name)
    except Exception as exception:
        await bot.close()
        raise exception


@bot.before_invoke
async def before_invoke(context: commands.Context):
    await context.typing()


if __name__ == '__main__':
    database_basis.createDatabase()
    bot.run(
        utility.getDiscordToken(),
        log_handler=None
    )
