import discord
from discord.ext import commands


class Slm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="slowmode", aliases=["slm"])
    @commands.has_guild_permissions(manage_guild=True)
    async def setdelay(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode in this channel to **{seconds}** seconds!")


def setup(client):
    client.add_cog(Slm(client))
