"""
Loader module for initializing the other scripts and modules.
Also stores them for use in the whole project directory.
"""

import discord
from commands.scripts import database
from commands.scripts import moderator
from commands.scripts import poll



def db_loaded():
    return db


def db_load():
    global db
    db = database.Database()


def client_loaded():
    return client


def client_load():
    global client
    print("Running: Client")
    client = discord.Client()


def moderator_loaded():
    return md


def moderator_load():
    global md
    md = moderator.Moderator()


def poll_loaded():
    return pl


def poll_load():
    global pl
    pl = poll.Poll()


db = None
client = None
md = None
pl = None
