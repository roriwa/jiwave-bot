#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import datetime
import sqlite3
import typing as t
import os.path as path
import logging

import discord

from . import models as m


DATABASE_PATH = path.abspath(path.join(
    path.dirname(__file__),
    '..',
    'database.sqlite'
))

logging.info(f"DB-Path: {DATABASE_PATH}")


def getConnection() -> sqlite3.Connection:
    logging.debug("Connection is created")
    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    connection.row_factory = sqlite3.Row
    ensureDatabase(connection)
    return connection


def ensureDatabase(conn: sqlite3.Connection):
    conn.executescript(r"""
    CREATE TABLE if not exists ChannelConfig (
        guild_id INTEGER,
        guild_name TEXT,
        channel_id INTEGER,
        channel_orig_name TEXT,
        target_time TIMESTAMP
    )
    
    CREATE TABLE if not exists GuildConfig (
        guild_id INTEGER,
        guild_name TEXT,
        message_template TEXT
    )
    """)


def listChannels(guild: discord.Guild) -> t.List[m.ChannelConfig]:
    with getConnection() as conn:
        cursor = conn.execute(
            "SELECT * FROM ChannelConfig WHERE guild_id = ?",
            [guild.id]
        )
        return [m.ChannelConfig(**row) for row in cursor.fetchall()]


def getChannelConfig(guild: discord.Guild, channel: discord.VoiceChannel) -> t.Optional[m.ChannelConfig]:
    with getConnection() as conn:
        cursor = conn.execute(
            "SELECT * FROM ChannelConfig WHERE guild_id = ? AND channel_id = ?",
            [guild.id, channel.id]
        )
        row = cursor.fetchone()
        if row:
            return m.ChannelConfig(**row)
        else:
            return None


def addOrUpdateChannel(guild: discord.Guild, channel: discord.VoiceChannel, date: datetime.datetime) -> m.ChannelConfig:
    config = getChannelConfig(guild=guild, channel=channel)
    with getConnection() as conn:
        if config:
            cursor = conn.execute(
                "UPDATE ChannelConfig SET target_time = ? WHERE guild_id = ? AND channel_id = ?",
                [date, guild.id, channel.id]
            )
        else:
            cursor = conn.execute(
                "INSERT INTO ChannelConfig VALUES (?, ?, ?, ?, ?)",
                [guild.id, guild.name, channel.id, channel.name, date]
            )
        conn.commit()

        return m.ChannelConfig(**conn.execute(
            "SELECT * FROM ChannelConfig WHERE rowid = ?",
            [cursor.lastrowid]
        ).fetchone())


def removeChannel(guild: discord.Guild, channel: discord.VoiceChannel) -> m.ChannelConfig:
    config = getChannelConfig(guild=guild, channel=channel)
    with getConnection() as conn:
        conn.execute(
            "DELETE FROM ChannelConfig WHERE guild_id = ? AND channel_id = ?",
            [guild.id, channel.id]
        )
        # conn.commit()
    return config


def setTimeFormat(guild: discord.Guild, message_template: str) -> m.GuildConfig:
    config = getGuildConfig(guild=guild)
    with getConnection() as conn:
        if config:
            cursor = conn.execute(
                "UPDATE ChannelConfig SET message_template = ? WHERE guild_id = ?",
                [message_template, guild.id]
            )
        else:
            cursor = conn.execute(
                "INSERT INTO GuildConfig VALUES (?, ?, ?)",
                [guild.id, guild.name, message_template]
            )
        conn.commit()

        return m.GuildConfig(**conn.execute(
            "SELECT * FROM ChannelConfig WHERE rowid = ?",
            [cursor.lastrowid]
        ).fetchone())


def getGuildConfig(guild: discord.Guild) -> t.Optional[m.GuildConfig]:
    with getConnection() as conn:
        cursor = conn.execute(
            "SELECT * FROM GuildConfig WHERE guild_id = ?",
            [guild.id]
        )
        row = cursor.fetchone()
        if row:
            return m.GuildConfig(**row)
        else:
            return None
