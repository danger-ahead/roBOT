import discord
import os
from decouple import config
from discord import channel
import  requests
import json
from duckduckgo_search import ddg
import wikipedia as wiki
import urllib
import quiz

client = discord.Client()
quiz = quiz.Quiz(client)

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
                data = json.loads(r.text)   #dict

                output = ''
                for key in data:
                    first_dict = key["phonetics"]
                    for phonetics in first_dict:
                        output += 'phonetics: '+phonetics["text"]+'\n'
                    
                    output += '\n'

                    first_dict = key["meanings"]
                    for meaning in first_dict:  #list
                        definitions = meaning["partOfSpeech"]
                        output += definitions + ' :\n'
                        definitions = meaning["definitions"] #list

                        i = 1
                        for definition in definitions:  #list
                            define = definition["definition"]
                            output += str(i) + '. ' +define + '\n'

                            try:
                                example = definition["example"]
                                output += 'example: '+example + '\n'
                            except:
                                pass

                            try:
                                synonyms = definition["synonyms"]
                                output += 'synonyms: '
                                for synonym in synonyms:
                                    output += synonym + ', '
                                output += '\n'
                            except:
                                pass
                            i += 1
                        output += '\n'

                await message.add_reaction('\U0001F44d')      
                await message.channel.send(output)
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

    elif message.content.lower().startswith('_math'):
        hold=message.content.find(' ')
        header = {'content-type': 'application/json'}
        querystring = urllib.parse.quote_plus(message.content[(hold+1):len(message.content)])
        result = requests.get("http://api.mathjs.org/v4/?expr="+querystring, headers=header)
        if result.status_code==200:
            await message.add_reaction('\U0001f44d')
            await message.channel.send(result.text)
        else:
            await message.add_reaction('\U0001F44E')
    
    elif message.content.lower().startswith('_search'):
        hold=message.content.find(' ')

        results = str(ddg(message.content[(hold+1):len(message.content)], region='wt-wt', safesearch='Off', time='y', max_results=1))
     
        index = results.find('\'body\'')
        await message.add_reaction('\U0001f44d')
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
         'x-rapidapi-key': config('RAPID_API'),
        'x-rapidapi-host': "genius.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        try:
            data=json.loads(response.text)
            response1=data["response"]
            hits=response1["hits"]

            for i in range (2):
                x=hits[i]
                y=x["result"]
                await message.channel.send('\''+y["full_title"]+'\''+'\nDetails of the song can be found at: '+y["url"])
            await message.add_reaction('\U0001f44d')
        except:
            await message.add_reaction('\U0001F44E')
        
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
        await message.reply('hi comrade'+'\U0001F44B'+'\ncontribute towards my well-being at https://github.com/danger-ahead/roBOT')

    elif message.content.startswith('_logoff'):
        await client.send_message(message.channel, 'Leaving server. BYE!')
        await client.close()
        exit()
        
    elif (message.content.startswith('_halt') or 
          message.content.startswith('_stop')):
        await quiz.stop(message,channel)
    elif (message.content.startswith('_reset')):
        await quiz.reset(channel)        
    elif (message.content.startswith('_quiz') or 
          message.content.startswith('_ask')):
        await quiz.start(message.channel)      
    elif (message.content.startswith('_scores')):
        await quiz.print_scores(channel)    
    elif (message.content.startswith('_next')):
        await quiz.next_question(message.channel)
    elif quiz is not None and quiz.started():
        #check if we have a question pending
        await quiz.answer_question(message,channel)
        #check quiz question correct

DISCORD_TOKEN=config('TOKEN')
client.run(DISCORD_TOKEN)