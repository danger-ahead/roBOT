import os
import json
import dotenv
import discord
import requests
from discord.ext import commands


dotenv.load_dotenv()


class F(commands.Cog):
    def __init__(self, client):
        self.client = client

    """
    ISSUE:
    idk how to use this
    and what does this command do
    
    """

    @commands.command()
    async def f(self, ctx):
        try:
            headers = {
                "x-rapidapi-key": str(os.getenv("RAPID_API")),
                "x-rapidapi-host": "numbersapi.p.rapidapi.com",
            }
            querystring = {"json": "true", "fragment": "true"}

            lst = ctx.message.content.split()

            if lst[1].find("y") != -1:
                year = lst[2]
                url = "https://numbersapi.p.rapidapi.com/" + year + "/year"

                response = requests.request(
                    "GET", url, headers=headers, params=querystring
                )
                if response.status_code == 200:
                    data = json.loads(response.text)
                    try:
                        embed = discord.Embed(
                            title="Date: " + data["date"],
                            description=data["text"],
                            color=discord.Color.blue(),
                        )

                        await ctx.send(embed=embed)
                        await ctx.message.add_reaction("\U0001f44d")
                    except:
                        embed = discord.Embed(
                            description=data["text"], color=discord.Color.blue()
                        )

                        await ctx.send(embed=embed)
                        await ctx.message.add_reaction("\U0001f44d")
                else:
                    await ctx.message.add_reaction("\U0001F44E")

            if lst[1].find("m") != -1:
                math = lst[2]
                url = "https://numbersapi.p.rapidapi.com/" + math + "/math"

                response = requests.request(
                    "GET", url, headers=headers, params=querystring
                )
                if response.status_code == 200:
                    data = json.loads(response.text)
                    embed = discord.Embed(
                        description=data["text"], color=discord.Color.blue()
                    )

                    await ctx.send(embed=embed)
                    await ctx.message.add_reaction("\U0001f44d")
                else:
                    await ctx.message.add_reaction("\U0001F44E")

        except Exception as e:
            await ctx.send(e)


def setup(client):
    client.add_cog(F(client))
