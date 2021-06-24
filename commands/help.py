"""
Module containing the function for _help command.
"""
import discord


async def help_call(discord, message):
    embed = discord.Embed(
        title="HELP",
        description="Use `_help <command name>` to find details about the command",
        color=discord.Color.blue(),
    )
    embed.add_field(
        name="**Administrator Commands**",
        value="configure, deconfigure, configconfess, deconfigconfess, kick, mute, unmute, moderation, leave, clean, trivia,\
         inspire, meme, wearesoftwareengineers",
        inline=False,
    )
    embed.add_field(
        name="**General Commands**",
        value="hi, contribute, mean, math, number_fact, year_fact, joke, weather, wiki, search, movie, song, confess, rank",
        inline=False,
    )
    embed.add_field(
        name="**Game Commands**",
        value="rolldice, tosscoin, poll",
        inline=False,
    )
    await message.channel.send(embed=embed)


async def config(discord, message):
    embed = discord.Embed(
        title="Configure",
        description="Configures roBOT to use a particular channel for admin commands",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$configure`")
    await message.channel.send(embed=embed)


async def deconfig(discord, message):
    embed = discord.Embed(
        title="Deconfigure",
        description="Deconfigures roBOT from using the configured channel for admin commands",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$deconfigure`")
    await message.channel.send(embed=embed)


async def configconfess(discord, message):
    embed = discord.Embed(
        title="Configconfess",
        description="Configures roBOT to use a particular channel for the confessions",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$configconfess`")
    await message.channel.send(embed=embed)


async def deconfigconfess(discord, message):
    embed = discord.Embed(
        title="Deconfigconfess",
        description="Deconfigures roBOT from using the configured confession channel for the confessions",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$deconfigconfess`")
    await message.channel.send(embed=embed)


async def kick(discord, message):
    embed = discord.Embed(
        title="Kick",
        description="roBOT kicks the mentioned user",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$kick @< user >`")
    await message.channel.send(embed=embed)


async def mute(discord, message):
    embed = discord.Embed(
        title="Mute",
        description="roBOT mutes the mentioned user",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$mute @< user >`")
    await message.channel.send(embed=embed)


async def trivia(discord, message):
    embed = discord.Embed(
        title="Trivia",
        description="Sends a trivia",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_trivia`")
    await message.channel.send(embed=embed)


async def wearesoftwareengineers(discord, message):
    embed = discord.Embed(
        title="Special command!",
        description="FOR ALL THE SOFTWARE ENGINEERS OUT THERE!",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_wearesoftwareengineers`")
    await message.channel.send(embed=embed)


async def inspire(discord, message):
    embed = discord.Embed(
        title="Inspire",
        description="Sends an inspirational quote which will surely enlighten you",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_inspire`")
    await message.channel.send(embed=embed)


async def meme(discord, message):
    embed = discord.Embed(
        title="Meme",
        description="Sends a meme from reddit",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_meme`")
    await message.channel.send(embed=embed)


async def unmute(discord, message):
    embed = discord.Embed(
        title="Unmute",
        description="roBOT unmutes the mentioned user",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$unmute @< user >`")
    await message.channel.send(embed=embed)


async def moderator(discord, message):
    embed = discord.Embed(
        title="Moderation",
        description="Instructs roBOT to activate chat moderation on the server",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$moderation`")
    await message.channel.send(embed=embed)


async def rank(discord, message):
    embed = discord.Embed(
        title="Rank",
        description="Tells the current friendship level of roBOT with the user",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$rank`")
    await message.channel.send(embed=embed)


async def leave(discord, message):
    embed = discord.Embed(
        title="Leave",
        description="Instructs roBOT to leave the server (works only in the channel configured with `$configure` command)",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$leave`")
    await message.channel.send(embed=embed)


async def clean(discord, message):
    embed = discord.Embed(
        title="Clean 🗑️",
        description="roBOT deletes the previous 100 chats from the channel",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`$clean`")
    await message.channel.send(embed=embed)


async def hi(discord, message):
    embed = discord.Embed(
        title="Hi 👋",
        description="Provides the user with a link to find roBOT's commands",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_hi`")
    await message.channel.send(embed=embed)


async def contribute(discord, message):
    embed = discord.Embed(
        title="Contribute 💻",
        description="Provides the user with a link to roBOT's source code",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_contribute`")
    await message.channel.send(embed=embed)


async def mean(discord, message):
    embed = discord.Embed(
        title="Mean 📚",
        description="Finds the meaning of the word",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_mean < word >`")
    await message.channel.send(embed=embed)


async def math(discord, message):
    embed = discord.Embed(
        title="Math 🧮",
        description="Solves the Math Problem",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_math < problem >`")
    await message.channel.send(embed=embed)


async def fm(discord, message):
    embed = discord.Embed(
        title="Number Fact 🔢",
        description="Tells an interesting fact about the number",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_f m < number >`")
    await message.channel.send(embed=embed)


async def fy(discord, message):
    embed = discord.Embed(
        title="Year Fact 🎆",
        description="Tells an interesting fact about the year",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_f y < year>`")
    await message.channel.send(embed=embed)


async def joke(discord, message):
    embed = discord.Embed(
        title="Joke 😆",
        description="Tells a joke",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_joke`")
    await message.channel.send(embed=embed)


async def wea(discord, message):
    embed = discord.Embed(
        title="Weather 🌤️",
        description="Tells the current weather situations of the city",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_wea < city, country code >`")
    await message.channel.send(embed=embed)


async def wiki(discord, message):
    embed = discord.Embed(
        title="Wiki 📖",
        description="Searches the Wikipedia for the query",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_wiki < query >`")
    await message.channel.send(embed=embed)


async def search(discord, message):
    embed = discord.Embed(
        title="Search 🔍",
        description="Searches DuckDuckGo for the query",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_search < query >`")
    await message.channel.send(embed=embed)


async def movie(discord, message):
    embed = discord.Embed(
        title="Movie 🎬",
        description="Tells the details of the movie",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_movie < movie >`")
    await message.channel.send(embed=embed)


async def songs(discord, message):
    embed = discord.Embed(
        title="Song 🎶",
        description="Tells the details of the song or finds the most famous song of the artist",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_song < song or artist >`")
    await message.channel.send(embed=embed)


async def confes(discord, message):
    embed = discord.Embed(
        title="Confess",
        description="roBOT deletes the user's confession message and forwards the confession message to configured confession channel anonymously",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_confess < confession >`")
    await message.channel.send(embed=embed)


async def rolldice(discord, message):
    embed = discord.Embed(
        title="Roll Dice 🎲",
        description="Rolls a dice",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_rolldice`")
    await message.channel.send(embed=embed)


async def tosscoin(discord, message):
    embed = discord.Embed(
        title="Toss Coin 🪙",
        description="Tosses a coin",
        color=discord.Color.blue(),
    )
    embed.add_field(name="**Syntax**", value="`_tosscoin`")
    await message.channel.send(embed=embed)


async def poll(discord, message):
    embed = discord.Embed(
        title="Poll 📊",
        description="Creates a poll and the users vote by reacting (clicking) on the respective choice's emoji",
        color=discord.Color.blue(),
    )
    embed.add_field(
        name="**Syntax**",
        value="`_poll < topic >,,< choice1 >,,< choice2 >,,...,,< upto choice9 >,,< poll duration >`",
    )
    await message.channel.send(embed=embed)


async def help(discord, message=None):

    cmd = message.content.split()
    try:
        function = helps[cmd[1]]
        exec(str(await eval(function + "(discord, message)")))
        await message.add_reaction("\U0001F44d")
    except IndexError:
        await help_call(discord, message)
        await message.add_reaction("\U0001F44d")


helps = {
    "help": "help_call",
    "configure": "config",
    "deconfigure": "deconfig",
    "configconfess": "configconfess",
    "deconfigconfess": "deconfigconfess",
    "kick": "kick",
    "mute": "mute",
    "unmute": "unmute",
    "moderation": "moderator",
    "leave": "leave",
    "clean": "clean",
    "hi": "hi",
    "contribute": "contribute",
    "mean": "mean",
    "math": "math",
    "inspire": "inspire",
    "number_fact": "fm",
    "year_fact": "fy",
    "joke": "joke",
    "weather": "wea",
    "wiki": "wiki",
    "search": "search",
    "movie": "movie",
    "song": "songs",
    "confess": "confes",
    "rank": "rank",
    "trivia": "trivia",
    "reset": "reset",
    "rolldice": "rolldice",
    "tosscoin": "tosscoin",
    "poll": "poll",
    "meme": "meme",
    "wearesoftwareengineers": "wearesoftwareengineers",
}
