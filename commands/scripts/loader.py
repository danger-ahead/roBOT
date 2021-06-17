import discord
from commands.scripts import database

def db_loaded():
    return db

def db_load():
    global db
    db = database.Database()

def client_loaded():
    return client

def client_load():
    global client
    client = discord.Client()

db = None
client = None