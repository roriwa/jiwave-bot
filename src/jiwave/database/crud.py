#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from .base import Session
from . import models as dbm
import discord


def createLogRecord(guild: discord.Guild, message: str):
    record = dbm.LogRecord(
        guild_id=guild.id,
        message=message
    )

    with Session() as session:
        session.add(record)
        session.commit()
