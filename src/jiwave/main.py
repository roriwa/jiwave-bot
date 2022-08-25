#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import configure_logging  # noqa
import logging
import os
import sys
import discord
from discord.ext.commands import Bot as DiscordBot, when_mentioned
from utility import logCalling


# this line removes a huge bug
# without this line this file is run two times (because of `import main`)
# that's why bot.run is not called and nothing would work
sys.modules['main'] = sys.modules['__main__']


bot = DiscordBot(
    command_prefix=when_mentioned,
    intents=discord.Intents.default()
)


@bot.event
async def on_error(*args):
    logging.error("on-error", exc_info=True)
    logging.error(str(args))


# @setup_hook is not possible, so we use this shortcut
@(lambda c: setattr(bot, c.__name__, c))
@logCalling
async def setup_hook():
    for plugin in os.listdir('plugins'):
        plugin = os.path.splitext(plugin)[0]
        if plugin.startswith('_'):
            continue

        logging.info(f"Importing {plugin}")
        await bot.load_extension(f'plugins.{plugin}')


if __name__ == '__main__':
    bot.run(
        os.getenv("DISCORD-TOKEN"),
        log_handler=None
    )