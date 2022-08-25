#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import logging
import logging.handlers as log_handlers
import os
from datetime import datetime


LOGGING_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'logs'
    )
)
if not os.path.isdir(LOGGING_PATH):
    os.mkdir(LOGGING_PATH)


class DiscordFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return not record.name.startswith("discord")


fileLoggingHandler = log_handlers.RotatingFileHandler(
    filename=os.path.join(
        LOGGING_PATH,
        f"jiwave.log"
    ),
    maxBytes=1024*1024*10,  # roughly 10mb
    backupCount=5,
    delay=True
)
# fileLoggingHandler.addFilter(DiscordFilter())

consoleLoggingHandler = logging.StreamHandler()
consoleLoggingHandler.addFilter(DiscordFilter())


logging.basicConfig(
    format="{asctime} | {levelname:.3} | {name:20} | {funcName:20} | {message}",
    style="{",
    level=logging.DEBUG,
    handlers=[
        fileLoggingHandler,
        consoleLoggingHandler
    ]
)


logging.info("=" * 100)
logging.info(f"Bot start at {datetime.now().isoformat(sep=' ', timespec='seconds')}")
logging.info("=" * 100)
