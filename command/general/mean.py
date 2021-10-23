import discord
import aiohttp
from discord.ext import commands
from command.database.loader import loader


class Mean(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mean(self, ctx, word):
        word_list = ctx.message.content.split()

        if len(word_list) > 2:  # user has more than 2 words as input
            await ctx.message.add_reaction("\U0001F44E")
        else:
            word = word_list[1]
            url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + word

            async with aiohttp.ClientSession() as session:
                Response = await session.get(url)
                if Response.status == 200:
                    data = await Response.json()

                    output = ""
                    for key in data:
                        first_dict = key["phonetics"]
                        for phonetics in first_dict:
                            output += "phonetics: " + phonetics["text"] + "\n"

                        output += "\n"

                        first_dict = key["meanings"]
                        for meaning in first_dict:  # list
                            definitions = meaning["partOfSpeech"]
                            output += definitions + " :\n"
                            definitions = meaning["definitions"]  # list

                            i = 1
                            for definition in definitions:  # list
                                define = definition["definition"]
                                output += str(i) + ". " + define + "\n"

                                try:
                                    example = definition["example"]
                                    output += "example: " + example + "\n"
                                except:
                                    pass

                                try:
                                    synonyms = definition["synonyms"]
                                    output += "synonyms: "
                                    for synonym in synonyms:
                                        output += synonym + ", "
                                    output += "\n"
                                except:
                                    pass
                                i += 1
                            output += "\n"

                    await ctx.message.add_reaction("\U0001F44d")
                    embed = discord.Embed(
                        title=word, description=output, color=discord.Color.blue()
                    )
                    await ctx.send(embed=embed)
                    db = loader.db_loaded()
                    await db.score_up(ctx, loader.client_loaded())
                else:
                    await ctx.message.add_reaction("\U0001F44E")


def setup(client):
    client.add_cog(Mean(client))
