import discord
from discord.ext import commands


class Slm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def slm(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(
            f"Setting the slowmode in this channel to **{seconds}** seconds!"
        )
        await ctx.message.add_reaction("\U0001f44d")

    @slm.error
    async def slm_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.reply("You don't have permission to use this command")
            await ctx.message.add_reaction("\U0001f44E")


def setup(client):
    client.add_cog(Slm(client))
