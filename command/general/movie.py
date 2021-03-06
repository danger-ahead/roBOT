import os
import json
import dotenv
import discord
import aiohttp
from discord.ext import commands
from command.database.loader import loader

dotenv.load_dotenv()


class Movie(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def movie(self, ctx, *, hold):
        querystring = {
            "query": hold,
            "page": "1",
        }

        headers = {
            "x-rapidapi-key": str(os.getenv("RAPID_API")),
            "x-rapidapi-host": "advanced-movie-search.p.rapidapi.com",
        }

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                "https://advanced-movie-search.p.rapidapi.com/search/movie",
                headers=headers,
                params=querystring,
            )

            data = await response.json()
            result_first = data["results"][0]

        try:
            embed = discord.Embed(
                title=result_first["original_title"],
                colour=discord.Color.blurple(),
                description=f"""
                
                **Release Date:** {result_first["release_date"]}
                **Original Language:** {result_first["original_language"]}

                **Overview:** {result_first["overview"]}
                """,
            )
            embed.set_image(url=result_first["poster_path"])
            await ctx.send(embed=embed)
            await ctx.message.add_reaction("\U0001f44d")
            db = loader.db_loaded()
            await db.score_up(ctx, loader.client_loaded())
        except:
            await ctx.message.add_reaction("\U0001F44E")


def setup(client):
    client.add_cog(Movie(client))
