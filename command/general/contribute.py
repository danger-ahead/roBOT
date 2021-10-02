import discord
from discord.ext import commands


class Contribute(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def contribute(self, ctx):
        embed = discord.Embed(  
            title = "Interested about open-source contribution ? ",
            description = """
                    Looks like you're interested to help my fellow amatuer creators in order to make
                    myself more polished and funky !!
                    Here's the link to repo: https://github.com/danger-ahead/roBOT
                    Feel free to give your suggestion as issues and submit PR requests with improvements!!
                    waiting for you PR peeps!! 
                    """,
            color = discord.Color.blue())

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("\U0001f44d")


def setup(client):
    client.add_cog(Contribute(client))