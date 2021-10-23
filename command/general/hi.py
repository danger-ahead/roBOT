import discord
from discord.ext import commands


class Hi(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hi(self, ctx):
        embed = discord.Embed(
            title="🙏🏻 Hello my friend!!, myself roBOT!",
            description="""An amatuer bot by amatuer Developer!! 😂
            Want to play with me?
            Visit: [Command List](https://github.com/danger-ahead/roBOT/blob/master/docs/COMMANDS.md)
            to know all commands I understand. \nI hope you're still here. Looking forward to spend some quality time with you.
            To know how you can improve my functionality use  `_contribute` """,
            color=discord.Color.blue(),
        )

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("\U0001f44d")


def setup(client):
    client.add_cog(Hi(client))
