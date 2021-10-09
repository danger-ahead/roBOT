import os
import json
import dotenv
import discord
import aiohttp
from discord.ext import commands
from command.database.loader import loader

dotenv.load_dotenv()


class F(commands.Cog):
    def __init__(self, client):
        self.client = client

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

                async with aiohttp.ClientSession() as session:
                    response = await session.get(
                        url, headers=headers, params=querystring
                    )
                    if response.status == 200:
                        data = await response.json()
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
                        db = loader.db_loaded()
                        await db.score_up(ctx, loader.client_loaded())
                    else:
                        await ctx.message.add_reaction("\U0001F44E")

            if lst[1].find("m") != -1:
                math = lst[2]
                url = "https://numbersapi.p.rapidapi.com/" + math + "/math"
                async with aiohttp.ClientSession() as session:
                    response = await session.get(
                        url, headers=headers, params=querystring
                    )
                    if response.status == 200:
                        data = await response.json()
                        embed = discord.Embed(
                            description=data["text"], color=discord.Color.blue()
                        )

                        await ctx.send(embed=embed)
                        await ctx.message.add_reaction("\U0001f44d")
                        db = loader.db_loaded()
                        await db.score_up(ctx, loader.client_loaded())
                    else:
                        await ctx.message.add_reaction("\U0001F44E")

        except:
            await ctx.message.add_reaction("\U0001f44E")


def setup(client):
    client.add_cog(F(client))
