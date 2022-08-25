#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from datetime import datetime as _datetime
from dataclasses import dataclass as _model


@_model
class ChannelConfig:
    guild_id: int
    guild_name: str
    channel_id: int
    channel_orig_name: str
    target_time: _datetime


@_model
class GuildConfig:
    guild_id: int
    guild_name: str
    message_template: str
