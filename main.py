import discord
import os
from decouple import config
import  requests
import json
from duckduckgo_search import ddg
import wikipedia as wiki

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('_confess'):
        await message.delete()

        hold=message.content.find(' ') #searches for the first space after the command
        
        embed=discord.Embed(title='Someone just confessed:', description=message.content[(hold+1):len(message.content)], color=discord.Color.blue())
        await message.channel.send(embed=embed)

    elif message.content.lower().startswith('_mean'):
        word_list = message.content.split()

        if(len(word_list) > 2): #user has more than 2 words as input
            await message.add_reaction('\U0001F44E')

        else:
            word = word_list[1]
            url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + word

            r = requests.get(url)
            if r.status_code==200: #checks status code of response received, 200 is the success code
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
                    await message.add_reaction('\U0001F44d')         
            else:
                await message.add_reaction('\U0001F44E')

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
            if response.status_code==200:
                data = json.loads(response.text)
                try:
                    await message.channel.send('Date: '+data["date"])
                    await message.channel.send(data["text"])
                    await message.add_reaction('\U0001f44d')
                except:
                    await message.channel.send(data["text"])
                    await message.add_reaction('\U0001f44d')
            else:
                await message.add_reaction('\U0001F44E')

        if lst[1].find('m') != -1:
            math = lst[2]
            url = "https://numbersapi.p.rapidapi.com/"+math+"/math"

            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.status_code==200:
                data = json.loads(response.text)
                await message.channel.send(data["text"])
                await message.add_reaction('\U0001f44d')
            else:
                await message.add_reaction('\U0001F44E')
    
    elif message.content.lower().startswith('_search'):
        hold=message.content.find(' ')

        results = str(ddg(message.content[(hold+1):len(message.content)], region='wt-wt', safesearch='Off', time='y', max_results=1))
     
        index = results.find('\'body\'')
        await message.channel.send(results[index+9:(len(results)-3)])

    elif message.content.lower().startswith('_movie'):
        url = "https://advanced-movie-search.p.rapidapi.com/search/movie"

        hold=message.content.find(' ')
        querystring = {"query":message.content[(hold+1):len(message.content)],"page":"1"}

        headers = {
            'x-rapidapi-key': config('RAPID_API'),
            'x-rapidapi-host': "advanced-movie-search.p.rapidapi.com"
            }

        result = requests.request("GET", url, headers=headers, params=querystring)

        data=json.loads(result.text)
        results=data["results"]
        try:
            result_first=results[0]
            await message.add_reaction('\U0001f44d')
        except:
            await message.add_reaction('\U0001F44E')

        await message.channel.send('Original title: '+result_first["original_title"]+'\nRelease date: '+result_first["release_date"]+'\nLanguage: '+result_first["original_language"])
        await message.channel.send(result_first["poster_path"])
        await message.channel.send('Overview: '+result_first["overview"])
    elif message.content.lower().startswith('_song'):
        url = "https://genius.p.rapidapi.com/search"
        hold=message.content.find(' ')
        querystring = {"q":message.content[(hold+1):len(message.content)]}

        headers = {
         'x-rapidapi-key': "SIGN-UP-FOR-KEY",
        'x-rapidapi-host': "genius.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data=json.loads(response.txt)
        response=data["response"]
        hits=response["hits"]
        

       
    elif message.content.lower().startswith('_wea'):
        city_list=message.content.split()
        city=''
        for i in range(1, len(city_list)):
            city=city+city_list[i]+' '

        newurl= "https://api.openweathermap.org/data/2.5/weather?" + "q="+ city +"&appid=" + config('OPEN_WEATHER_TOKEN') 
        response=requests.get(newurl)

        if response.status_code==200:
            response=response.json()
            weatherrep=response['main']
            temperature = weatherrep['temp']
            report = response['weather']
            humidity = weatherrep['humidity']
            report_description=str({report[0]['description']})
            index=report_description.find('\'')
            index2=report_description.find('\'',2)
            await message.channel.send(report_description[(index+1):index2]+'\nTemp. is '+str('%.2f'%(temperature-273))+'℃'+'\nHumidity is '+str(humidity)+'%')
            await message.add_reaction('\U0001f44d')
        else:
            await message.add_reaction('\U0001F44E')

    elif message.content.lower().startswith('_wiki'):
        hold=message.content.find(' ')
        try:
            await message.channel.send(wiki.summary(message.content[(hold+1):len(message.content)], sentences=4))
            await message.add_reaction('\U0001f44d')
        except:
            await message.add_reaction('\U0001F44E')

    elif message.content.lower().startswith('_hi'):
        await message.reply('hi'+'\U0001F44B'+'\ncontribute towards my well-being at https://github.com/danger-ahead/roBOT')

DISCORD_TOKEN=config('TOKEN')
client.run(DISCORD_TOKEN)