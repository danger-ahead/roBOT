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

    if message.content.lower().startswith('_mean'):
        word_list = message.content.split()

        if(len(word_list) > 2): #user has more than 2 words as input
            await message.channel.send('Enter a single word at a time :/')

        else:
            word = word_list[1]
            try:
                url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + word
                r = requests.get(url)
                data = json.loads(r.text)[0]           

                for definitions in (data["meanings"]):
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

        headers = {
            'x-rapidapi-key': config('RAPID_API'),
            'x-rapidapi-host': "numbersapi.p.rapidapi.com"
            }
        
        querystring = {"json":"true","fragment":"true"}

        lst = message.content.split()

        if lst[1].find('y') != -1:
            year = lst[2]
            url = "https://numbersapi.p.rapidapi.com/"+year+"/year"            

            response = requests.request("GET", url, headers=headers, params=querystring)
            data = json.loads(response.text)
            try:
                await message.channel.send('Date: '+data["date"])
                await message.channel.send(data["text"])
            except:
                await message.channel.send(data["text"])

        if lst[1].find('m') != -1:
            math = lst[2]
            url = "https://numbersapi.p.rapidapi.com/"+math+"/math"

            response = requests.request("GET", url, headers=headers, params=querystring)
            data = json.loads(response.text)
            try:
                await message.channel.send(data["text"])
            except:
                await message.channel.send('Was that even a number? :/')
    
    elif message.content.lower().startswith('_search'):
        hold = 0
        for i in range(0, len(message.content)):
            if message.content[i] == ' ':
                hold = i
                break

        results = str(ddg(message.content[hold:len(message.content)], region='wt-wt', safesearch='Off', time='y', max_results=1))
     
        index = results.find('\'body\'')
        await message.channel.send(results[index+9:(len(results)-3)])

    elif message.content.lower().startswith('_confess'):
        await message.delete()

        hold = 0
        for i in range(0, len(message.content)):
            if message.content[i] == ' ':
                hold = i
                break

        embed=discord.Embed(title='Someone just confessed:', description=message.content[hold:len(message.content)], color=discord.Color.blue())
        await message.channel.send(embed=embed)

    elif message.content.lower().startswith('_movie'):
        url = "https://advanced-movie-search.p.rapidapi.com/search/movie"

        hold = 0
        for i in range(0, len(message.content)):
            if message.content[i] == ' ':
                hold = i
                break
        querystring = {"query":message.content[hold:len(message.content)],"page":"1"}

        headers = {
            'x-rapidapi-key': config('RAPID_API'),
            'x-rapidapi-host': "advanced-movie-search.p.rapidapi.com"
            }

        result = requests.request("GET", url, headers=headers, params=querystring)
        data=json.loads(result.text)
        results=data["results"]
        result_first=results[0]

        await message.channel.send('Original title: '+result_first["original_title"]+'\nRelease date: '+result_first["release_date"]+'\nLanguage: '+result_first["original_language"])
        await message.channel.send(result_first["poster_path"])
        await message.channel.send('Overview: '+result_first["overview"])

DISCORD_TOKEN=config('TOKEN')
client.run(DISCORD_TOKEN)