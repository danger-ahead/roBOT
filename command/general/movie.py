import os
import json
import dotenv
import discord
import aiohttp
from discord.ext import commands

dotenv.load_dotenv()

class Movie(commands.Cog):
    def __init__(self, client):
        self.client = client

    """
    ISSUE:
    this needs api key ig,
    someone please test it with api key
    """

    @commands.command()
    async def movie(self, ctx):
        hold = ctx.message.content.find(" ")
        querystring = {
            "query": ctx.message.content[(hold + 1) : len(ctx.message.content)],
            "page": "1",
        }

        headers = {
            "x-rapidapi-key": str(os.getenv("RAPID_API")),
            "x-rapidapi-host": "advanced-movie-search.p.rapidapi.com",
        }

        async with aiohttp.ClientSession() as session:
            response = await session.get("https://advanced-movie-search.p.rapidapi.com/search/movie",
                                        headers = headers, params=querystring)
            
            data = await response.json()
            result_first = data['results'][0]
        
        try:
            await ctx.message.add_reaction("\U0001f44d")
        except:
            await ctx.message.add_reaction("\U0001F44E")

        embed = discord.Embed(
            title = result_first["original_title"],
            colour = discord.Color.blurple(),
            description = f"""
            
            **Release Date:** {result_first["release_date"]}
            **Original Language:** {result_first["original_language"]}

            **Overview:** {result_first["overview"]}
            """
        )
        embed.set_image(url = result_first["poster_path"])

        await ctx.send(embed = embed)
        
def setup(client):
    client.add_cog(Movie(client))