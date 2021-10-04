"""
Loader module for initializing the other scripts and modules.
Also stores them for use in the whole project directory.
"""

from discord.ext import commands
import discord
from command.database.loader import database
from  command.game import poll



def db_loaded():
    return db


def db_load():
    global db
    db = database.Database()


# def poll_loaded():
#     return pl


# def poll_load():
#     global pl
#     pl = poll.Poll()

# creates instance of client here, so that the instance can be accessed through out the project
def client_loaded():
    return client


def client_load():
    global client
    print("Running: Client")
    # enabling intents
    intents = discord.Intents.all()

    # defining discord client
    client = commands.Bot(command_prefix = "_", intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name=f"_help"))


db = None
# pl = None
client = None
