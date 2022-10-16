#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import datetime as dt
from sqlalchemy import Column, String, Integer, DateTime
from .base import Base as BaseModel


class TimerConfig(BaseModel):
    __tablename__ = "timer-config"

    guild_id: int | Column = Column(Integer, nullable=False, primary_key=True)
    channel_id: int | Column = Column(Integer, nullable=False, primary_key=True, unique=True)
    channel_orig_name: str | Column = Column(String, nullable=False)
    target_time: dt.datetime | Column = Column(DateTime, nullable=False)


class ArchiveConfig(BaseModel):
    __tablename__ = "archive-config"

    guild_id: int | Column = Column(Integer, nullable=False, primary_key=True)
    source_id: int | Column = Column(Integer, nullable=False, primary_key=True, unique=True)
    target_id: int | Column = Column(Integer, nullable=False)
    emoticon: str | Column = Column(String, nullable=False)
    count: int | Column = Column(Integer, nullable=False)


class ArchiveMessage(BaseModel):
    __tablename__ = "archive-messages"

    message_id: int | Column = Column(Integer, primary_key=True)
    archive_id: int | Column = Column(Integer, primary_key=True)
    timestamp: dt.datetime | Column = Column(DateTime, primary_key=True, default=dt.datetime.now)


class GuildConfig(BaseModel):
    __tablename__ = "guild-config"

    guild_id: int | Column = Column(Integer, primary_key=True, unique=True)
    message_template: str | Column = Column(String, nullable=False, default="{time}")


class LogRecord(BaseModel):
    __tablename__ = "logs"

    guild_id: int | Column = Column(Integer, primary_key=True)
    timestamp: dt.datetime | Column = Column(DateTime, primary_key=True, default=dt.datetime.now)
    message: str | Column = Column(String, nullable=False)
