import os
import urllib
import json
import  requests
import random
import discord
from decouple import config
from discord import channel
from duckduckgo_search import ddg
import wikipedia as wiki
import quiz
from scripts import poll
from scripts import database
from scripts import moderator
from scripts import games

# creates instances of the different modules in use
db = database.Database()
poll = poll.Poll()
client = discord.Client()
quiz = quiz.Quiz(client)
moderator = moderator.Moderator()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random%22)
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
                          
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    # sets roBOT's status to 'Listening to _hi'
    activity = discord.Activity(type=discord.ActivityType.listening, name="_hi")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

# checks if the message begins with '_' (bot command)
    if message.content.startswith('_'):
        if message.content.lower().startswith('_confess'):
            await message.delete()
            hold = message.content.find(' ') #searches for the first space after the command
            await db.confess(client, discord, message.content[(hold+1):len(message.content)], message)
            await db.score_up(message, client)

        elif message.content.lower().startswith('_hi'):
                embed = discord.Embed(title='Hello comrade!!, Meet myself roBOT!',
                description='an amatuer bot by amatuer Developers!! XD \
                \n The full list of commands \
                can be found here: \n https://github.com/RccTechz/roBOT/blob/master/docs/COMMANDS.md \n\
                have a great time interacting and having fun with me!!\n for details about how to contribute to \
                this bot use  \'_contribute\' ', color=discord.Color.blue())
                await message.channel.send(embed=embed)

        elif message.content.lower().startswith('_contribute'):
                embed = discord.Embed(title='Interested about open-source contribution ? ',
                description='Looks like you\'re interested to help my fellow amatuer creators in order to make\
                    myself more polished and funky !!\n Here\'s the link to repo: https://github.com/RccTechz/roBOT\
                        \n Feel free to give your suggestion as issues and submit PR requests with improvements!!\
                        \n waiting for you PR peeps!! ', color=discord.Color.blue())
                await message.channel.send(embed=embed)
                
        elif message.content.startswith("_inspire"):
                quote=get_quote();
                await message.channel.send(quote)

        elif message.content.lower().startswith('_mean'):
            word_list = message.content.split()

            if len(word_list) > 2: #user has more than 2 words as input
                await message.add_reaction('\U0001F44E')

            else:
                word = word_list[1]
                url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + word

                r = requests.get(url)
                if r.status_code == 200: #checks status code of response received, 200 is success code
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
                    embed = discord.Embed(title=word, description=output, color=discord.Color.blue())
                    await message.channel.send(embed=embed)
                else:
                    await message.add_reaction('\U0001F44E')

            await db.score_up(message, client)

        elif message.content.lower().startswith('_covrep'):
            query = message.content[8:]
            url = "https://coronavirus-map.p.rapidapi.com/v1/spots/week"
            querystring = {"region":query}
            headers = {
            'x-rapidapi-key': config('RAPID_API'),
            'x-rapidapi-host': "coronavirus-map.p.rapidapi.com"
            }
            try:
                response = requests.request("GET", url, headers=headers, params=querystring)
                json_data = json.loads(response.text)
                count = 0
                rpt = ""
                for key in json_data['data']:
                    copy = str(key)
                    prevnum = 0
                    prevnum = int(copy[8:10])-1
                    prevstr = copy[0:8]
                    prev = prevstr+str(prevnum)
                    diffcase = json_data['data'][str(key)]['total_cases']-json_data['data'][str(prev)]['total_cases']
                    diffdeath = json_data['data'][str(key)]['deaths']-json_data['data'][prev]['deaths']
                    if diffcase < 0:
                        diffcase = 0
                    if diffdeath < 0:
                        diffdeath = 0
                    rpt = str(rpt) + str("\n"+'Covid report of date : ' + str(key) +
                    '\n'+'Total No of Cases: '+str(json_data['data'][str(key)]['total_cases'])+' ,'+
                    ' Deaths: '+str(json_data['data'][str(key)]['deaths'])+' ,'+
                    ' Recoverd: '+str(json_data['data'][str(key)]['recovered'])+' ,'+
                    ' Tested: '+str(json_data['data'][str(key)]['tested']))+' ,'+' New Cases: '+str(diffcase)+' ,'+' New Deaths: '+str(diffdeath)+'\n'
                    count = count+1
                    if count == 5:
                        embed = discord.Embed(title="Covid stats of : "
                        +query.capitalize(), description=rpt, color=discord.Color.blue())

                        await message.channel.send(embed=embed)
                        break
                await message.add_reaction('\U0001F44d')
            except:
                await message.add_reaction('\U0001F44E')

            await db.score_up(message, client)

        elif message.content.lower().startswith('_f'):
            headers = {
                'x-rapidapi-key': config('RAPID_API'),
                'x-rapidapi-host': "numbersapi.p.rapidapi.com"
                }
            querystring = {"json":"true", "fragment":"true"}

            lst = message.content.split()

            if lst[1].find('y') != -1:
                year = lst[2]
                url = "https://numbersapi.p.rapidapi.com/"+year+"/year"

                response = requests.request("GET", url, headers=headers, params=querystring)
                if response.status_code == 200:
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
                if response.status_code == 200:
                    data = json.loads(response.text)
                    await message.channel.send(data["text"])
                    await message.add_reaction('\U0001f44d')
                else:
                    await message.add_reaction('\U0001F44E')

            await db.score_up(message, client)

        elif message.content.lower().startswith('_math'):
            hold = message.content.find(' ')
            header = {'content-type': 'application/json'}
            querystring = urllib.parse.quote_plus(message.content[(hold+1):len(message.content)])
            result = requests.get("http://api.mathjs.org/v4/?expr="+querystring, headers=header)
            if result.status_code == 200:
                await message.add_reaction('\U0001f44d')
                await message.channel.send(result.text)
            else:
                await message.add_reaction('\U0001F44E')

            await db.score_up(message, client)

        elif message.content.lower().startswith('_joke'):
            querystring = {"api_key":config('RANDOM_STUFF_API')}
            headers = {
                'x-rapidapi-key': config('RAPID_API'),
                'x-rapidapi-host': "random-stuff-api.p.rapidapi.com"
                }
            try:
                response = requests.request("GET", "https://random-stuff-api.p.rapidapi.com/joke/any",
                headers=headers, params=querystring)
                data = json.loads(response.text)
                if data["type"] == 'single':
                    await message.channel.send(data["joke"])
                elif data["type"] == 'twopart':
                    await message.channel.send(data["setup"]+'\n'+data["delivery"])
                await message.channel.send('category: '+data["category"])
                await message.add_reaction('\U0001f44d')
            except:
                await message.add_reaction('\U0001F44E')

        elif message.content.lower().startswith('_poll'):
            await message.delete()
            await poll._create_poll(discord, message)
            await db.score_up(message, client)

        elif message.content.lower().startswith('_rolldice'):
            await games.roll_a_dice(message)
            await message.add_reaction('\U0001f44d')
            await db.score_up(message, client)

        elif message.content.lower().startswith('_tosscoin'):
            await games.toss_coin(message)
            await message.add_reaction('\U0001f44d')
            await db.score_up(message, client)

        elif message.content.lower().startswith('_search'):
            hold = message.content.find(' ')

            results = str(ddg(message.content[(hold+1):len(message.content)], region='wt-wt',
            safesearch='Off', time='y', max_results=1))

            index = results.find('\'body\'')
            await message.add_reaction('\U0001f44d')
            embed = discord.Embed(title="Search results for : "
            +(message.content[(hold+1):len(message.content)]),
            description=results[index+9:(len(results)-3)], color=discord.Color.blue())
            await message.channel.send(embed=embed)

            await db.score_up(message, client)

        elif message.content.lower().startswith('_movie'):
            hold = message.content.find(' ')
            querystring = {"query":message.content[(hold+1):len(message.content)], "page":"1"}

            headers = {
                'x-rapidapi-key': config('RAPID_API'),
                'x-rapidapi-host': "advanced-movie-search.p.rapidapi.com"
                }

            result = requests.request("GET", "https://advanced-movie-search.p.rapidapi.com/search/movie",
            headers=headers, params=querystring)

            data = json.loads(result.text)
            results = data["results"]
            try:
                result_first = results[0]
                await message.add_reaction('\U0001f44d')
            except:
                await message.add_reaction('\U0001F44E')

            await message.channel.send('Original title: '+result_first["original_title"]+
            '\nRelease date: '+result_first["release_date"]+'\nLanguage: '+
            result_first["original_language"])

            await message.channel.send(result_first["poster_path"])
            await message.channel.send('Overview: '+result_first["overview"])

            await db.score_up(message, client)

        elif message.content.lower().startswith('_song'):
            hold = message.content.find(' ')
            querystring = {"q":message.content[(hold+1):len(message.content)]}

            headers = {
            'x-rapidapi-key': config('RAPID_API'),
            'x-rapidapi-host': "genius.p.rapidapi.com"
            }

            response = requests.request("GET", "https://genius.p.rapidapi.com/search",
            headers=headers, params=querystring)
            try:
                data = json.loads(response.text)
                response1 = data["response"]
                hits = response1["hits"]

                for i in range(1):
                    x = hits[i]
                    y = x["result"]
                    await message.channel.send('\''+y["full_title"]+'\''+
                    '\nDetails of the song can be found at: '+y["url"])
                await message.add_reaction('\U0001f44d')
            except:
                await message.add_reaction('\U0001F44E')

            await db.score_up(message, client)

        elif message.content.lower().startswith('_wea'):
            city_list = message.content.split()
            city = ''
            for i in range(1, len(city_list)):
                city = city+city_list[i]+' '

            newurl = "https://api.openweathermap.org/data/2.5/weather?"+ \
            "q="+ city +"&appid=" + config('OPEN_WEATHER_TOKEN')
            response = requests.get(newurl)

            if response.status_code == 200:
                response = response.json()
                weatherrep = response['main']
                temperature = weatherrep['temp']
                report = response['weather']
                humidity = weatherrep['humidity']
                report_description = str({report[0]['description']})
                index = report_description.find('\'')
                index2 = report_description.find('\'', 2)
                embed = discord.Embed(title="Weather update for :  "+city,
                description=report_description[(index+1):index2]+
                '\nTemp. is '+str('%.2f'%(temperature-273))+'℃'+'\nHumidity is '+str(humidity)+'%',
                color=discord.Color.blue())
                await message.channel.send(embed=embed)
                await message.add_reaction('\U0001f44d')
            else:
                await message.add_reaction('\U0001F44E')

            await db.score_up(message, client)

        if message.content.startswith('_rank'):
            await db.rank_query(message)

        elif message.content.lower().startswith('_wiki india'):
            embed = discord.Embed(title="India",
            description='India, country that occupies the greater part of South Asia. \
            It is a constitutional republic that represents a highly diverse population consisting of\
                thousands of ethnic groups. Its capital is New Delhi. With roughly one-sixth of \
                    the world\'s total population, it is the second most populous country, after China.'
                    , color=discord.Color.blue())
            await message.channel.send(embed=embed)
            await db.score_up(message, client)

        elif message.content.lower().startswith('_wiki'):
            hold = message.content.find(' ')
            try:
                embed = discord.Embed(title=message.content[(hold+1):len(message.content)],
                description=wiki.summary(message.content[(hold+1):len(message.content)], sentences=4),
                color=discord.Color.blue())
                await message.channel.send(embed=embed)
                await message.add_reaction('\U0001f44d')
            except:
                await message.add_reaction('\U0001F44E')

            await db.score_up(message, client)

        elif message.content.startswith('_qstop'):
            await quiz.stop(message.channel)

        elif message.content.startswith('_reset'):
            await quiz.reset(message.channel)

        elif message.content.startswith('_quiz'):
            await quiz.start(message.channel)
            await db.score_up(message, client)

        elif message.content.startswith('_scores'):
            await quiz.print_scores(message.channel)

        elif message.content.startswith('_next'):
            await quiz.next_question(message.channel)

        elif quiz is not None and quiz.started():
            #check if we have a question pending
            await quiz.answer_question(message, channel)
            #check quiz question correct

    #admin command block
    elif message.content.startswith('$'):
        #checks for administrator rights
        if message.author.guild_permissions.administrator:
            if message.content.lower().startswith('$clean'):
                await message.channel.purge(limit=100)
                await db.score_up(message, client)

            elif message.content.startswith('$mute'):
                if (message.mentions.__len__()>0):
                    for user in message.mentions:
                        user = await message.guild.query_members(user_ids=[user.id])
                    user = user[0]

                    try:
                        await user.edit(mute = True)
                    except Exception:
                        await message.channel.send('User\'s not connected to voice!')

            elif message.content.startswith('$unmute'):
                if (message.mentions.__len__()>0):
                    for user in message.mentions:
                        user = await message.guild.query_members(user_ids=[user.id])
                    user = user[0]
                    try:
                        await user.edit(mute = False)
                    except Exception:
                        await message.channel.send('User\'s not connected to voice!')

            elif message.content.startswith('$kick'):
                if (message.mentions.__len__()>0):
                    for user in message.mentions:
                        user = await message.guild.query_members(user_ids=[user.id])
                    user = user[0]
                    await user.kick(reason='Kicked by roBOT!')

            elif message.content.startswith('$configure'):
                await db.server_config(message.guild.id, message)

            elif message.content.startswith('$configconfess'):
                await db.confess_config(message.guild.id, message)

            elif message.content.startswith('$moderation'):
                await db.moderation_service(message.guild.id, message)

            elif message.content.startswith('$deconfigure'):
                await db.server_deconfig(message.guild.id, message)

            elif message.content.startswith('$deconfigconfess'):
                await db.confess_deconfig(message.guild.id, message)
            elif message.content.startswith('$leave'):
                await db.leave_server(message.guild.id, message)

        else:   #message author doesn't have admin rights
            await message.channel.send('<@'+str(message.author.id)+'> Do you\'ve admin rights?')

    if await db.check_server_moderation(message.guild.id) == 1:
        await moderator.check(message)

DISCORD_TOKEN = config('TOKEN')
client.run(DISCORD_TOKEN)
