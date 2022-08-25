#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import functools
import logging
import traceback
from asyncio import iscoroutinefunction


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
                logging.error(f"{func.__name__} failed with {exc.__class__.__qualname__}")
                traceback.print_exception(type(exc), exc, exc.__traceback__)
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
                logging.error(f"{func.__name__} failed with {exc.__class__.__qualname__}")
                traceback.print_exception(type(exc), exc, exc.__traceback__)
            else:
                logging.debug(msg_on_stop)

        return functionWrapper
    else:
        raise TypeError(f"{func} is no function or coroutine")
