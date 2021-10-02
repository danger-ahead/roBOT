import discord
from discord.ext import commands
from duckduckgo_search import ddg

class Search(commands.Cog):
    def __init__(self, client):
        self.client = client

    """
    ISSUE:
    it returns a dict
    and not the first result.
    someone fix it who is familiar with ddg
    """


    @commands.command()
    async def search(self, ctx):
        hold = ctx.message.content.find(" ")
        results = str(
            ddg(
                ctx.message.content[(hold + 1) : len(ctx.message.content)],
                region="wt-wt",
                safesearch="Off",
                time="y",
                max_results=1,
            )
        )
        index = results.find("'body'")
        embed = discord.Embed(
            title="Search results for : "
            + (ctx.message.content[(hold + 1) : len(ctx.message.content)]),
            description=results[index + 9 : (len(results) - 3)],
            color=discord.Color.blue(),
        )

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("\U0001f44d")


def setup(client):
    client.add_cog(Search(client))