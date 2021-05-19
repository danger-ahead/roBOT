import discord
import os
from decouple import config
import  requests
import json
from duckduckgo_search import ddg

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

    elif message.content.lower().startswith('_mean'):
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
                    definitions2 = "&"+ str(definitions2)+"&"
                    definitions2 = definitions2.split(", ")                                       
                    define = definitions2[0]
                    define=define.replace("&[{", "")
                    define=define.replace("}]&", "")
                    lomba=len(define)
                    if(define[lomba-1]==""):
                        define=define+"\'"
                    elif((define[lomba-1]!="\"")or(define[lomba-1]!="\'")):
                        define=define+"\'"

                    await message.channel.send(define)
                    

            except:
                await message.channel.send('Didn\'t find the word :/')

    elif message.content.lower().startswith('_f'):

        fact_token=config('NUMBERS_API')
        headers = {
            'x-rapidapi-key': fact_token,
            'x-rapidapi-host': "numbersapi.p.rapidapi.com"
            }
        
        querystring = {"json":"true","fragment":"true"}

        lst = message.content.split()

        if lst[1].find('y') != -1:
            year = lst[2]
            url = "https://numbersapi.p.rapidapi.com/"+year+"/year"            

            response = requests.request("GET", url, headers=headers, params=querystring)
            data = json.loads(response.text)
            pairs = data.items()
            try:
                data2 = (data["date"])
                await message.channel.send('Date: '+data2)
                data3 = (data["text"])
                await message.channel.send(data3)
            except:
                data3 = (data["text"])
                await message.channel.send(data3)

        if lst[1].find('m') != -1:
            math = lst[2]
            url = "https://numbersapi.p.rapidapi.com/"+math+"/math"

            response = requests.request("GET", url, headers=headers, params=querystring)
            data = json.loads(response.text)
            pairs = data.items()
            try:
                data2 = (data["text"])
                await message.channel.send(data2)
            except:
                await message.channel.send('Was that even a number? :/')
    
    elif message.content.lower().startswith('_search'):
        hold = 0
        for i in range(0, len(message.content)):
            if message.content[i] == ' ':
                hold = i
                break

        search_term = message.content[hold:len(message.content)]

        results = str(ddg(search_term, region='wt-wt', safesearch='Off', time='y', max_results=1))
     
        index = results.find('\'body\'')
        result = results[index+9:(len(results)-3)]
        await message.channel.send(result)

    elif message.content.startswith('_confess'):
        await message.delete()

        hold = 0
        for i in range(0, len(message.content)):
            if message.content[i] == ' ':
                hold = i
                break

        embed=discord.Embed(title='Someone just confessed:', description=message.content[hold:len(message.content)], color=discord.Color.blue())
        await message.channel.send(embed=embed)       

DISCORD_TOKEN=config('TOKEN')
client.run(DISCORD_TOKEN)