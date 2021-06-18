import os
import discord
from decouple import config
from discord import channel
import quiz
from commands import *
from commands.scripts import loader

# creates instances of the different modules in use
loader.db_load()
loader.moderator_load()
loader.poll_load()
loader.client_load()

db = loader.db_loaded()
moderator = loader.moderator_loaded()
poll = loader.poll_loaded()
client = loader.client_loaded()
# quiz = quiz.Quiz(client)


@client.event
async def on_ready():
    print("\nWe have logged in as {0.user}".format(client))

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
            "_confess": "confess_rank.confess",
            "_rank": "confess_rank.rank"
        }

        if commands.get(message.content[: message.content.find(" ")]) == None:
            command = commands.get(message.content)
        else:
            command = commands.get(message.content[: message.content.find(" ")])

        exec(str(await eval(command + "(discord, message)")))
        await db.score_up(message, client)

    elif message.content.startswith("$"):
        if message.author.guild_permissions.administrator:
            commands = {
                "$clean": "admin_commands.clean",
                "$moderation": "admin_commands.moderation",
                "$configure": "admin_commands.configure",
                "$deconfigure": "admin_commands.deconfigure",
                "$leave": "admin_commands.leave",
                "$mute": "admin_commands.mute",
                "$unmute": "admin_commands.unmute",
                "$kick": "admin_commands.kick",
                "$configconfess": "admin_commands.configconfess",
                "$deconfigconfess": "admin_commands.deconfigconfess"
            }

            if commands.get(message.content[: message.content.find(" ")]) == None:
                command = commands.get(message.content)
            else:
                command = commands.get(message.content[: message.content.find(" ")])

            exec(str(await eval(command + "(message)")))
            await db.score_up(message, client)

        else:  # message author doesn't have admin rights
            await message.channel.send(
                "<@" + str(message.author.id) + "> Do you've admin rights?"
            )

    # # checks if the message begins with '_' (bot command)
    # elif message.content.startswith("_"):
    #     if message.content.lower().startswith("_joke"):
    #         querystring = {"api_key": config("RANDOM_STUFF_API")}
    #         headers = {
    #             "x-rapidapi-key": config("RAPID_API"),
    #             "x-rapidapi-host": "random-stuff-api.p.rapidapi.com",
    #         }
    #         try:
    #             response = requests.request(
    #                 "GET",
    #                 "https://random-stuff-api.p.rapidapi.com/joke/any",
    #                 headers=headers,
    #                 params=querystring,
    #             )
    #             data = json.loads(response.text)
    #             if data["type"] == "single":
    #                 await message.channel.send(data["joke"])
    #             elif data["type"] == "twopart":
    #                 await message.channel.send(data["setup"] + "\n" + data["delivery"])
    #             await message.channel.send("category: " + data["category"])
    #             await message.add_reaction("\U0001f44d")
    #         except:
    #             await message.add_reaction("\U0001F44E")

    #     elif message.content.startswith("_qstop"):
    #         await quiz.stop(message.channel)

    #     elif message.content.startswith("_reset"):
    #         await quiz.reset(message.channel)

    #     elif message.content.startswith("_quiz"):
    #         await quiz.start(message.channel)
    #         await db.score_up(message, client)

    #     elif message.content.startswith("_scores"):
    #         await quiz.print_scores(message.channel)

    #     elif message.content.startswith("_next"):
    #         await quiz.next_question(message.channel)

    #     elif quiz is not None and quiz.started():
    #         # check if we have a question pending
    #         await quiz.answer_question(message, channel)
    #         # check quiz question correct

    if await db.check_server_moderation(message.guild.id) == 1:
        await moderator.check(message)


DISCORD_TOKEN = config("TOKEN")
client.run(DISCORD_TOKEN)
