"""
Module containing the functions for _wiki and _search commands.
"""

from duckduckgo_search import ddg
import wikipedia as wiki


async def wikipedia(discord, message):
    hold = message.content.find(" ")
    try:
        embed = discord.Embed(
            title=message.content[(hold + 1) : len(message.content)],
            description=wiki.summary(
                message.content[(hold + 1) : len(message.content)], sentences=4
            ),
            color=discord.Color.blue(),
        )
        await message.channel.send(embed=embed)
        await message.add_reaction("\U0001f44d")
    except:
        await message.add_reaction("\U0001F44E")


async def search(discord, message):
    hold = message.content.find(" ")
    results = str(
        ddg(
            message.content[(hold + 1) : len(message.content)],
            region="wt-wt",
            safesearch="Off",
            time="y",
            max_results=1,
        )
    )
    index = results.find("'body'")
    await message.add_reaction("\U0001f44d")
    embed = discord.Embed(
        title="Search results for : "
        + (message.content[(hold + 1) : len(message.content)]),
        description=results[index + 9 : (len(results) - 3)],
        color=discord.Color.blue(),
    )
    await message.channel.send(embed=embed)
