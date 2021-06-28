import discord
from decouple import config
from commands import *
from commands.scripts import *

loader.db_load()  # loads database
loader.moderator_load()  # loads moderator
loader.poll_load()  # loads poll
loader.client_load()  # loads client

db = loader.db_loaded()
moderator = loader.moderator_loaded()
poll = loader.poll_loaded()
client = loader.client_loaded()


@client.event
async def on_ready():
    print("\nWe have logged in as {0.user}".format(client))

    # sets roBOT's status to 'Listening to _help'
    activity = discord.Activity(type=discord.ActivityType.listening, name="_help")
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("_"):
        # if the command message is a single word message, takes the whole message
        if commands.get(message.content[: message.content.find(" ")]) == None:
            command = commands.get(message.content)
        # if the command message is a multi word message, takes only the 1st word
        else:
            command = commands.get(message.content[: message.content.find(" ")])

        exec(str(await eval(command + "(discord, message)")))
        await db.score_up(message, client)  # levels up the author of the message

    elif message.content.startswith("$"):
        if message.author.guild_permissions.administrator:
            if commands.get(message.content[: message.content.find(" ")]) == None:
                command = commands.get(message.content)
            else:
                command = commands.get(message.content[: message.content.find(" ")])

            exec(str(await eval(command + "(message)")))
            await db.score_up(message, client)
            await message.add_reaction("\U0001f44d")

        else:  # message author doesn't have admin rights
            await message.channel.send(
                "<@" + str(message.author.id) + "> Do you've admin rights?"
            )
            await message.add_reaction("\U0001f44E")

    # check if the server is configured for moderation
    if await db.check_server_moderation(message.guild.id) == 1:
        # checks the words of the message to moderate
        await moderator.check(message)


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
    "_wearesoftwareengineers": "api_commands.programming_joke",
    "_meme": "api_commands.meme",
    "_trivia": "api_commands.trivia",
    "_ptrivia": "api_commands.ptrivia",
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


DISCORD_TOKEN = config("TOKEN")
client.run(DISCORD_TOKEN)
