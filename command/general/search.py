import json
import discord
from discord.ext import commands
from duckduckgo_search import ddg
from command.database.loader import loader


class Search(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def search(self, ctx, *, query):

        results = ddg(query, region="in-en", safesearch="Off", time="y", max_results=1)[
            0
        ]
        data = json.loads(str(results).replace("'", '"'))

        embed = discord.Embed(
            title=data["title"],
            color=discord.Color.blue(),
            description=data["body"],
            url=data["href"],
        )

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("\U0001f44d")
        db = loader.db_loaded()
        await db.score_up(ctx, loader.client_loaded())


def setup(client):
    client.add_cog(Search(client))
