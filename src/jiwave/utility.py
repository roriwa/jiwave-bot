#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import functools
import logging
import os
from asyncio import iscoroutinefunction


def localFile(*paths):
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            *paths
        )
    )


def logCalling(func):
    msg_on_start = f"{func.__name__} is being called"
    msg_on_stop = f"{func.__name__} is done running"

    if iscoroutinefunction(func):

        @functools.wraps(func)
        async def coroutineWrapper(*args, **kwargs):
            logging.debug(msg_on_start)
            try:
                await func(*args, **kwargs)
            except Exception as exc:
                logging.error(f"{func.__name__} failed with {exc.__class__.__qualname__}", exc_info=exc)
            else:
                logging.debug(msg_on_stop)

        return coroutineWrapper
    elif callable(func):

        @functools.wraps(func)
        def functionWrapper(*args, **kwargs):
            logging.debug(msg_on_start)
            try:
                func(*args, **kwargs)
            except Exception as exc:
                logging.error(f"{func.__name__} failed with {exc.__class__.__qualname__}", exc_info=exc)
            else:
                logging.debug(msg_on_stop)

        return functionWrapper
    else:
        raise TypeError(f"{func} is no function or coroutine")


def getDiscordToken() -> str:
    environ_key = os.getenv('DISCORD-TOKEN')
    token_file = __getTokenFilePath()
    if environ_key:
        logging.info("loading 'discord-token from environment")
        return environ_key
    elif token_file and os.path.isfile(token_file):
        logging.info(f"loading discord-token from file ({token_file})")
        with open(token_file, 'r') as file:
            return file.readline()
    else:
        raise EnvironmentError('missing environment variable or token file (see README.md)')


def __getTokenFilePath():
    for level in range(3):
        fp = localFile(*(['..'] * level), 'DISCORD-TOKEN.txt')
        if os.path.isfile(fp):
            return fp
    return None
