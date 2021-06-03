import discord
import os
from decouple import config
from discord import channel
import  requests
import json
from duckduckgo_search import ddg
import wikipedia as wiki
import urllib
import database
import quiz


db = database.Database()
client = discord.Client()
quiz = quiz.Quiz(client)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity=discord.Activity(type=discord.ActivityType.listening, name="_hi")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('_confess'):
        await message.delete()
        hold=message.content.find(' ') #searches for the first space after the command
        await db.confess(client, discord, message.content[(hold+1):len(message.content)], message)
        await db.score_up(message.author.id, message, channel, client)

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
                embed=discord.Embed(title=word,description=output,color=discord.Color.blue())      
                await message.channel.send(embed=embed)
            else:
                await message.add_reaction('\U0001F44E')

        await db.score_up(message.author.id, message, channel, client) 
    elif message.content.startswith('_covrep'):
      
       query = message.content[8:]
       url = "https://coronavirus-map.p.rapidapi.com/v1/spots/week"
       querystring = {"region":query}
       headers = {
        'x-rapidapi-key': config('RAPID_API'),
        'x-rapidapi-host': "coronavirus-map.p.rapidapi.com"
       }
       response = requests.request("GET", url, headers=headers, params=querystring)
       json_data = json.loads(response.text)
       count=0
       rpt=""
       for key in json_data['data']:
         rpt= str(rpt) +str("\n"+'Covid report of date : ' + str(key) + '\n' + 'Total No of Cases: ' + str(json_data['data'][str(key)]['total_cases']) + ' ,' + 'Deaths: '+ str(json_data['data'][str(key)]['deaths']) + ' ,' + 'Recoverd: ' + str(json_data['data'][str(key)]['recovered'])+' ,' + 'Tested: ' + str(json_data['data'][str(key)]['tested']))
        
         count=count+1
         if count==5:
             embed=discord.Embed(title = "Covid stats of : "+ query.capitalize(),description=rpt,color=discord.Color.blue())

             await message.channel.send(embed=embed)
             break

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

        await db.score_up(message.author.id, message, channel, client)

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

        await db.score_up(message.author.id, message, channel, client)

    elif message.content.lower().startswith('_joke'):
        querystring = {"api_key":config('RANDOM_STUFF_API')}
        headers = {
            'x-rapidapi-key': "b1264b02bfmsh99f6f8bebf118abp137ec8jsnb3ed934770cb",
            'x-rapidapi-host': "random-stuff-api.p.rapidapi.com"
            }
        try:
            response = requests.request("GET", "https://random-stuff-api.p.rapidapi.com/joke/any", headers=headers, params=querystring)
            data=json.loads(response.text)
            if data["type"] == 'single':
                await message.channel.send(data["joke"])
            elif data["type"] == 'twopart':
                await message.channel.send(data["setup"]+'\n'+data["delivery"])
            await message.channel.send('category: '+data["category"])
            await message.add_reaction('\U0001f44d')
        except:
            await message.add_reaction('\U0001F44E')
    
    elif message.content.lower().startswith('_drive'):
        hold1 = message.content.find(' ')
        hold2 = message.content.find('--')
        place=[]
        place.append(message.content[(hold1+1):(hold2-1)].strip())
        place.append(message.content[(hold2+3):len(message.content)].strip())
        
        lat=[]
        lon=[]
        try:
            data = {
                'key': config('LOCATION_IQ'),
                'q': place[0],
                'format': 'json'
            }
            result = requests.get("https://us1.locationiq.com/v1/search.php", params=data)
            data=json.loads(result.text)[0]
            lat.append(float(data['lat']))
            lon.append(float(data['lon']))
            data = {
                'key': config('LOCATION_IQ'),
                'q': place[1],
                'format': 'json'
            }
            result2 = requests.get("https://us1.locationiq.com/v1/search.php", params=data)
            data=json.loads(result2.text)[0]
            lat.append(float(data['lat']))
            lon.append(float(data['lon']))

            body = {"locations":[[lon[1],lat[1]],[lon[0],lat[0]]],"metrics":["distance"],"units":"km"}

            headers = {
                'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
                'Authorization': config('OPEN_ROUTE_SERVICE'),
                'Content-Type': 'application/json; charset=utf-8'
            }
            call = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers)
            data = json.loads(call.text)
            if str(data['distances'][0][1])=='0.0':
                await message.channel.send('Not reachable by car :/')
                await message.add_reaction('\U0001f44E')
            else:
                await message.channel.send(str(data['distances'][0][1])+' km')
                await message.add_reaction('\U0001f44d')
        except:
            await message.add_reaction('\U0001f44E')

        await db.score_up(message.author.id, message, channel, client)

    elif message.content.lower().startswith('_search'):
        hold=message.content.find(' ')

        results = str(ddg(message.content[(hold+1):len(message.content)], region='wt-wt', safesearch='Off', time='y', max_results=1))
     
        index = results.find('\'body\'')
        await message.add_reaction('\U0001f44d')
        embed=discord.Embed(title="Search results for : "+(message.content[(hold+1):len(message.content)]),description=results[index+9:(len(results)-3)],color=discord.Color.blue())
        await message.channel.send(embed=embed)

        await db.score_up(message.author.id, message, channel, client)

    elif message.content.lower().startswith('_movie'):
        hold=message.content.find(' ')
        querystring = {"query":message.content[(hold+1):len(message.content)],"page":"1"}

        headers = {
            'x-rapidapi-key': config('RAPID_API'),
            'x-rapidapi-host': "advanced-movie-search.p.rapidapi.com"
            }

        result = requests.request("GET", "https://advanced-movie-search.p.rapidapi.com/search/movie", headers=headers, params=querystring)

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

        await db.score_up(message.author.id, message, channel, client)

    elif message.content.lower().startswith('_song'):
        hold=message.content.find(' ')
        querystring = {"q":message.content[(hold+1):len(message.content)]}

        headers = {
         'x-rapidapi-key': config('RAPID_API'),
        'x-rapidapi-host': "genius.p.rapidapi.com"
        }

        response = requests.request("GET", "https://genius.p.rapidapi.com/search", headers=headers, params=querystring)
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

        await db.score_up(message.author.id, message, channel, client)
        
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

        await db.score_up(message.author.id, message, channel, client)
    if message.content.startswith('_wiki india') or message.content.startswith('_wiki India'):
        embed=discord.Embed(title="India",description= 'India, country that occupies the greater part of South Asia. It is a constitutional republic that represents a highly diverse population consisting of thousands of ethnic groups. Its capital is New Delhi. With roughly one-sixth of the world\'s total population, it is the second most populous country, after China.' , color=discord.Color.blue())
        await message.channel.send(embed=embed)


    elif message.content.lower().startswith('_wiki'):
        hold=message.content.find(' ')
        try:
            
            embed=discord.Embed(title=message.content[(hold+1):len(message.content)], description=wiki.summary(message.content[(hold+1):len(message.content)], sentences=4),color=discord.Color.blue())
            await message.channel.send(embed=embed)
            await message.add_reaction('\U0001f44d')
        except:
            await message.add_reaction('\U0001F44E')

        await db.score_up(message.author.id, message, channel, client)

    elif message.content.lower().startswith('_hi'):
        embed=discord.Embed(title='Hello comrade!!, Meet myself roBOT!', description= 'an amatuer bot by amatuer Developers!! XD \n The full list of commands can be found here: \n https://github.com/danger-ahead/roBOT/blob/master/docs/COMMANDS.md \n have a great time interacting and having fun with me!!\n for details about how to contribute to this bot use  \'_contribute\' ' , color=discord.Color.blue())
        await message.channel.send(embed=embed)
        await db.score_up(message.author.id, message, channel, client)

    elif message.content.lower().startswith('_contribute'):
        embed=discord.Embed(title='Interested about open-source contribution ? ', description= 'Looks like you are interested to help my fellow amatuer creators in order to make myself more polished and funky !!\n Here is the link to my repo: https://github.com/danger-ahead/roBOT \n Feel free to give your suggestion as issues and submit PR requests with improvements!! \n waiting for you PR peeps!! ' , color=discord.Color.blue())
        await message.channel.send(embed=embed)
        await db.score_up(message.author.id, message, channel, client)

    elif message.content.startswith('_leave'):
        await db.leave_server(message.guild.id, message.channel.id, message)
        
    elif message.content.startswith('_qstop'):
        await quiz.stop(message,channel)

    elif (message.content.startswith('_reset')):
        await quiz.reset(channel)

    elif message.content.startswith('_quiz'):
        await quiz.start(message.channel)

        await db.score_up(message.author.id, message, channel, client)

    elif (message.content.startswith('_scores')):
        await quiz.print_scores(channel)

    elif (message.content.startswith('_next')):
        await quiz.next_question(message.channel)

    elif quiz is not None and quiz.started():
        #check if we have a question pending
        await quiz.answer_question(message,channel)
        #check quiz question correct

    elif message.content.startswith('_rank'):
        await db.rank_query(message.author.id, message, channel)

    elif message.content.startswith('_configure'):
        await db.server_config(message.guild.id, message.channel.id, message)
    

    elif message.content.startswith('_configconfess'):
        await db.confess_config(message.guild.id, message.channel.id, message)

    elif message.content.startswith('_deconfigure'):
        await db.server_deconfig(message.guild.id, message.channel.id, message)

    elif message.content.startswith('_deconfigconfess'):
        await db.confess_deconfig(message.guild.id, message.channel.id, message)

DISCORD_TOKEN=config('TOKEN')
client.run(DISCORD_TOKEN)