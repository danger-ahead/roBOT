import os
import json
import requests
import random
import discord
from decouple import config
from discord import channel
import quiz

# from scripts import poll
# from commands.scripts import database

# from scripts import moderator
# from scripts import games
from commands import *
from commands.scripts import *

# creates instances of the different modules in use
loader.db_load()
loader.client_load()
db = loader.db_loaded()
poll = poll.Poll()
client = loader.client_loaded()
quiz = quiz.Quiz(client)
moderator = moderator.Moderator()


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
            "_poll": "poll._create_poll",
            "_rolldice": "games.roll_a_dice",
            "_tosscoin": "games.toss_coin",
            "_help": "help.help",
            "_confess": "confess.confess"
        }

        if commands.get(message.content[: message.content.find(" ")]) == None:
            command = commands.get(message.content)
        else:
            command = commands.get(message.content[: message.content.find(" ")])

        exec(str(await eval(command + "(discord, message)")))
        await db.score_up(message, client)

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
