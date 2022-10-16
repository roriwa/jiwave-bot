#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import datetime
from sqlalchemy import Column, String, Integer, DateTime
from .base import Base as BaseModel


class TimerConfig(BaseModel):
    __tablename__ = "timer-config"

    guild_id = Column(Integer, nullable=False, primary_key=True)
    channel_id = Column(Integer, nullable=False, primary_key=True, unique=True)
    channel_orig_name = Column(String, nullable=False)
    target_time = Column(DateTime, nullable=False)


class ArchiveConfig(BaseModel):
    __tablename__ = "archive-config"

    guild_id = Column(Integer, nullable=False, primary_key=True)
    source_id = Column(Integer, nullable=False, primary_key=True, unique=True)
    target_id = Column(Integer, nullable=False)
    emoticon = Column(String, nullable=False)
    count = Column(Integer, nullable=False)


class ArchiveMessage(BaseModel):
    __tablename__ = "archive-messages"

    message_id = Column(Integer, primary_key=True)
    archive_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, primary_key=True, default=datetime.datetime.utcnow)


class GuildConfig(BaseModel):
    __tablename__ = "guild-config"

    guild_id = Column(Integer, primary_key=True, unique=True)
    message_template = Column(String, nullable=False)


class LogRecord(BaseModel):
    __tablename__ = "logs"

    guild_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, primary_key=True, default=datetime.datetime.utcnow)
    message = Column(String, nullable=False)
