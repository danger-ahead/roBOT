import os
import json
import requests
import random
import discord
from decouple import config
from discord import channel
import quiz

# from scripts import poll
from commands.scripts import database

# from scripts import moderator
# from scripts import games
from commands import *

# creates instances of the different modules in use
db = database.Database()
# poll = poll.Poll()
client = discord.Client()
quiz = quiz.Quiz(client)
# moderator = moderator.Moderator()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

    # sets roBOT's status to 'Listening to _hi'
    activity = discord.Activity(type=discord.ActivityType.listening, name="_hi")
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("_"):
        commands = {
            "_hi": "hi_contrib.hi",
            "_contribute": "hi_contrib.contrib",
            "_covrep": "api_commands.covrep",
            "_f": "api_commands.f",
            "_movie": "api_commands.movie",
            "_song": "api_commands.song",
            "_search": "wiki_search.search",
            "_wiki": "wiki_search.wikipedia",
            "_math": "api_commands.math",
            "_mean": "api_commands.mean",
            "_wea": "api_commands.wea",
            "_inspire": "api_commands.inspire",
        }

        if commands.get(message.content[: message.content.find(" ")]) == None:
            command = commands.get(message.content)
        else:
            command = commands.get(message.content[: message.content.find(" ")])

        exec(await eval(command + "(discord, message)"))

    # checks if the message begins with '_' (bot command)
    elif message.content.startswith("_"):
        if message.content.lower().startswith("_confess"):
            await message.delete()
            hold = message.content.find(
                " "
            )  # searches for the first space after the command
            await db.confess(
                client,
                discord,
                message.content[(hold + 1) : len(message.content)],
                message,
            )
            await db.score_up(message, client)

        elif message.content.lower().startswith("_joke"):
            querystring = {"api_key": config("RANDOM_STUFF_API")}
            headers = {
                "x-rapidapi-key": config("RAPID_API"),
                "x-rapidapi-host": "random-stuff-api.p.rapidapi.com",
            }
            try:
                response = requests.request(
                    "GET",
                    "https://random-stuff-api.p.rapidapi.com/joke/any",
                    headers=headers,
                    params=querystring,
                )
                data = json.loads(response.text)
                if data["type"] == "single":
                    await message.channel.send(data["joke"])
                elif data["type"] == "twopart":
                    await message.channel.send(data["setup"] + "\n" + data["delivery"])
                await message.channel.send("category: " + data["category"])
                await message.add_reaction("\U0001f44d")
            except:
                await message.add_reaction("\U0001F44E")

        elif message.content.lower().startswith("_poll"):
            await message.delete()
            await poll._create_poll(discord, message)
            await db.score_up(message, client)

        elif message.content.lower().startswith("_rolldice"):
            await games.roll_a_dice(message)
            await message.add_reaction("\U0001f44d")
            await db.score_up(message, client)

        elif message.content.lower().startswith("_tosscoin"):
            await games.toss_coin(message)
            await message.add_reaction("\U0001f44d")
            await db.score_up(message, client)

        if message.content.startswith("_rank"):
            await db.rank_query(message)

        elif message.content.startswith("_qstop"):
            await quiz.stop(message.channel)

        elif message.content.startswith("_reset"):
            await quiz.reset(message.channel)

        elif message.content.startswith("_quiz"):
            await quiz.start(message.channel)
            await db.score_up(message, client)

        elif message.content.startswith("_scores"):
            await quiz.print_scores(message.channel)

        elif message.content.startswith("_next"):
            await quiz.next_question(message.channel)

        elif quiz is not None and quiz.started():
            # check if we have a question pending
            await quiz.answer_question(message, channel)
            # check quiz question correct

        # Help command
        elif message.content.lower().startswith("_help"):

            cmd = message.content.split()

            try:
                # Administrator Commands
                if cmd[1] == "configure":
                    embed = discord.Embed(
                        title="configure",
                        description="Configures roBOT to use a particular channel for admin commands",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$configure`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "deconfigure":
                    embed = discord.Embed(
                        title="deconfigure",
                        description="Deconfigures roBOT from using the configured channel for admin commands",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$deconfigure`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "configconfess":
                    embed = discord.Embed(
                        title="configconfess",
                        description="Configures roBOT to use a particular channel for the confessions",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$configconfess`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "deconfigconfess":
                    embed = discord.Embed(
                        title="deconfigconfess",
                        description="Deconfigures roBOT from using the configured confession channel for the confessions",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$deconfigconfess`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "kick":
                    embed = discord.Embed(
                        title="kick",
                        description="roBOT kicks the mentioned user",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$kick @< user >`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "mute":
                    embed = discord.Embed(
                        title="mute",
                        description="roBOT mutes the mentioned user",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$mute @< user >`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "unmute":
                    embed = discord.Embed(
                        title="unmute",
                        description="roBOT unmutes the mentioned user",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$unmute @< user >`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "moderation":
                    embed = discord.Embed(
                        title="moderation",
                        description="Instructs roBOT to activate chat moderation on the server",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$moderation`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "rank":
                    embed = discord.Embed(
                        title="rank",
                        description="Tells the current friendship level of roBOT with the user",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$rank`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "leave":
                    embed = discord.Embed(
                        title="leave",
                        description="Instructs roBOT to leave the server (works only in the channel configured with `$configure` command)",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$leave`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "clean":
                    embed = discord.Embed(
                        title="clean",
                        description="roBOT deletes the previous 100 chats from the channel",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`$clean`")
                    await message.channel.send(embed=embed)

                # General Commands
                elif cmd[1] == "hi":
                    embed = discord.Embed(
                        title="hi",
                        description="Provides the user with a link to find roBOT's commands",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_hi`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "contribute":
                    embed = discord.Embed(
                        title="contribute",
                        description="Provides the user with a link to roBOT's source code",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_contribute`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "mean":
                    embed = discord.Embed(
                        title="mean",
                        description="Finds the meaning of the word",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_mean < word >`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "math":
                    embed = discord.Embed(
                        title="math",
                        description="Solves the Math Problem",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_math < problem >`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "f" and cmd[2] == "m":
                    embed = discord.Embed(
                        title="f m",
                        description="Tells an interesting fact about the number",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_f m < number >`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "f" and cmd[2] == "y":
                    embed = discord.Embed(
                        title="f y",
                        description="Tells an interesting fact about the year",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_f y < year>`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "joke":
                    embed = discord.Embed(
                        title="joke",
                        description="Tells a joke",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_joke`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "wea":
                    embed = discord.Embed(
                        title="wea",
                        description="Tells the current weather situations of the city",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(
                        name="**Syntax**", value="`_wea < city, country code >`"
                    )
                    await message.channel.send(embed=embed)

                elif cmd[1] == "wiki":
                    embed = discord.Embed(
                        title="wiki",
                        description="Searches the Wikipedia for the query",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_wiki < query >`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "search":
                    embed = discord.Embed(
                        title="search",
                        description="Searches DuckDuckGo for the query",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_search < query >`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "movie":
                    embed = discord.Embed(
                        title="movie",
                        description="Tells the details of the movie",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_movie < movie >`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "song":
                    embed = discord.Embed(
                        title="song",
                        description="Tells the details of the song or finds the most famous song of the artist",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(
                        name="**Syntax**", value="`_song < song or artist >`"
                    )
                    await message.channel.send(embed=embed)

                elif cmd[1] == "confess":
                    embed = discord.Embed(
                        title="confess",
                        description="roBOT deletes the user's confession message and forwards the confession message to configured confession channel anonymously",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(
                        name="**Syntax**", value="`_confess < confession >`"
                    )
                    await message.channel.send(embed=embed)

                elif cmd[1] == "quiz":
                    embed = discord.Embed(
                        title="quiz",
                        description="Starts quiz",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_quiz`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "qstop":
                    embed = discord.Embed(
                        title="qstop",
                        description="Stops an ongoing quiz",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_qstop`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "scores":
                    embed = discord.Embed(
                        title="scores",
                        description="Tells the current scores of the quiz participants",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_scores`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "next":
                    embed = discord.Embed(
                        title="next",
                        description="Skips to the next question in quiz",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_next`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "reset":
                    embed = discord.Embed(
                        title="reset",
                        description="Resets the quiz",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_reset`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "rolldice":
                    embed = discord.Embed(
                        title="rolldice",
                        description="Rolls a dice",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_rolldice`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "tosscoin":
                    embed = discord.Embed(
                        title="tosscoin",
                        description="Tosses a coin",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(name="**Syntax**", value="`_tosscoin`")
                    await message.channel.send(embed=embed)

                elif cmd[1] == "poll":
                    embed = discord.Embed(
                        title="poll",
                        description="Creates a poll and the users vote by reacting (clicking) on the respective choice's emoji",
                        color=discord.Color.blue(),
                    )
                    embed.add_field(
                        name="**Syntax**",
                        value="`_poll < topic >,,< choice1 >,,< choice2 >,,...,,< upto choice9 >,,< poll duration >`",
                    )
                    await message.channel.send(embed=embed)

            except:
                embed = discord.Embed(
                    title="HELP",
                    description="Use `_help <command name>` to find details about the command",
                    color=discord.Color.blue(),
                )
                embed.add_field(
                    name="**Administrator Commands**",
                    value="configure, deconfigure, configconfess, deconfigconfess, kick, mute, unmute, moderation, rank, leave, clean",
                    inline=False,
                )
                embed.add_field(
                    name="**General Commands**",
                    value="hi, contribute, mean, math, f m, f y, joke, wea, wiki, search, movie, song, confess",
                    inline=False,
                )
                embed.add_field(
                    name="**Quiz Commands**",
                    value="quiz, qstop, scores, next, reset",
                    inline=False,
                )
                embed.add_field(
                    name="**Game Commands**",
                    value="rolldice, tosscoin, poll",
                    inline=False,
                )
                await message.channel.send(embed=embed)

    # admin command block
    elif message.content.startswith("$"):
        # checks for administrator rights
        if message.author.guild_permissions.administrator:
            if message.content.lower().startswith("$clean"):
                await message.channel.purge(limit=100)
                await db.score_up(message, client)

            elif message.content.startswith("$mute"):
                if message.mentions.__len__() > 0:
                    for user in message.mentions:
                        user = await message.guild.query_members(user_ids=[user.id])
                    user = user[0]

                    try:
                        await user.edit(mute=True)
                    except Exception:
                        await message.channel.send("User's not connected to voice!")

            elif message.content.startswith("$unmute"):
                if message.mentions.__len__() > 0:
                    for user in message.mentions:
                        user = await message.guild.query_members(user_ids=[user.id])
                    user = user[0]
                    try:
                        await user.edit(mute=False)
                    except Exception:
                        await message.channel.send("User's not connected to voice!")

            elif message.content.startswith("$kick"):
                if message.mentions.__len__() > 0:
                    for user in message.mentions:
                        user = await message.guild.query_members(user_ids=[user.id])
                    user = user[0]
                    await user.kick(reason="Kicked by roBOT!")

            elif message.content.startswith("$configure"):
                await db.server_config(message.guild.id, message)

            elif message.content.startswith("$configconfess"):
                await db.confess_config(message.guild.id, message)

            elif message.content.startswith("$moderation"):
                await db.moderation_service(message.guild.id, message)

            elif message.content.startswith("$deconfigure"):
                await db.server_deconfig(message.guild.id, message)

            elif message.content.startswith("$deconfigconfess"):
                await db.confess_deconfig(message.guild.id, message)
            elif message.content.startswith("$leave"):
                await db.leave_server(message.guild.id, message)

        else:  # message author doesn't have admin rights
            await message.channel.send(
                "<@" + str(message.author.id) + "> Do you've admin rights?"
            )

    if await db.check_server_moderation(message.guild.id) == 1:
        await moderator.check(message)


DISCORD_TOKEN = config("TOKEN")
client.run(DISCORD_TOKEN)
