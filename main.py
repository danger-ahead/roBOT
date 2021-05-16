import discord
import os
from decouple import config

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('fuckYouSHOHOM'):
        await message.channel.send('YEAH FUCK HIM')

DISCORD_TOKEN=config('TOKEN')
client.run(DISCORD_TOKEN)