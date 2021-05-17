import discord
import os
from decouple import config
import  requests
import json

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('roBOT LETS GET TO WORK'):
        await message.channel.send('HECK YEAH')

    if message.content.startswith('_mean'):

        word_list = message.content.split()

        if(len(word_list) > 2): #user has more than 2 words as input
            await message.channel.send('I can\'t search the meaning of 2 words simultaneously')

        else:
            st = ''
            word = word_list[1]
            url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + word
            r = requests.get(url)
            data = json.loads(r.text)[0]
            pairs = data.items()
            data2 = (data["meanings"])

            for definitions in data2:
                st = st + str(definitions)
                st = st + '\n\n'
            
            await message.channel.send(st)   

DISCORD_TOKEN=config('TOKEN')
client.run(DISCORD_TOKEN)