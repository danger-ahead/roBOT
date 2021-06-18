import os
import discord
from decouple import config
from discord import channel
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
            "_rank": "confess_rank.rank",
            "_joke": "api_commands.joke",
            "_meme": "api_commands.meme",
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
                "$deconfigconfess": "admin_commands.deconfigconfess",
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

    # elif message.content.startswith("_"):
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
