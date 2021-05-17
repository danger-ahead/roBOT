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
            await message.channel.send('Enter a single word at a time :/')

        else:
            word = word_list[1]
            try:
                url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + word
                r = requests.get(url)
                data = json.loads(r.text)[0]
                pairs = data.items()
                data2 = (data["meanings"])

                for definitions in data2:
                    definitions2 = (definitions["definitions"])
                    definitions2 = str(definitions2)
                    definitions2 = definitions2.split("\'")
                    define = definitions2[3]
                    await message.channel.send(define)

            except:
                await message.channel.send('Didn\'t find the word :/')

DISCORD_TOKEN=config('TOKEN')
client.run(DISCORD_TOKEN)