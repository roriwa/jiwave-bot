#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from sqlalchemy import Column, String, Integer, DateTime
from .base import Base as BaseModel


class ChannelConfig(BaseModel):
    __tablename__ = "channel-config"

    guild_id = Column(Integer)
    channel_id = Column(Integer)
    channel_orig_name = Column(String)
    target_time: DateTime


class GuildConfig(BaseModel):
    __tablename__ = "guild-config"

    guild_id = Column(Integer, primary_key=True, unique=True)
    message_template = Column(String, nullable=False)


class LogRecord(BaseModel):
    __tablename__ = "logs"

    guild_id = Column(Integer, primary_key=True)
    timestamp = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
