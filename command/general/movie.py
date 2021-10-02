import json
import requests
from decouple import config
from discord.ext import commands

class Movie(commands.Cog):
    def __init__(self, client):
        self.client = client

    """
    ISSUE:
    this needs api key ig,
    someone please test it with api key
    """

    @commands.command()
    async def movie(self, ctx, search : str):
        hold = ctx.message.content.find(" ")
        querystring = {
            "query": search,
            "page": "1",
        }

        headers = {
            "x-rapidapi-key": config("RAPID_API"),
            "x-rapidapi-host": "advanced-movie-search.p.rapidapi.com",
        }

        result = requests.request(
            "GET",
            "https://advanced-movie-search.p.rapidapi.com/search/movie",
            headers=headers,
            params=querystring,
        )

        data = json.loads(result.text)
        results = data["results"]
        try:
            result_first = results[0]
            await ctx.message.add_reaction("\U0001f44d")
        except:
            await ctx.message.add_reaction("\U0001F44E")

        await ctx.send(
            "Original title: "
            + result_first["original_title"]
            + "\nRelease date: "
            + result_first["release_date"]
            + "\nLanguage: "
            + result_first["original_language"]
        )

        await ctx.send(result_first["poster_path"])
        await ctx.send("Overview: " + result_first["overview"])




def setup(client):
    client.add_cog(Movie(client))