import discord
from discord.ext import commands
import datetim

class Lock_Unlock(commands.Cog):

    def __init__(self, client):
        self.client = client

@commands.command(name="lockchannel", aliases=['lock'])
    @commands.has_guild_permissions(manage_channels = True)
    async def lockchannel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        for role in ctx.guild.roles:
            if role.permissions.administrator:
                await channel.set_permissions(role, send_messages=True, read_messages=True)
            elif role.name == "@everyone":
                await channel.set_permissions(role, send_messages=False)

        await ctx.send(f"🔒The channel {channel.mention} has been locked")

    @commands.command(name="unlockchannel", aliases=['unlock'])
    @commands.has_guild_permissions(manage_channels = True)
    async def unlockchannel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        await channel.set_permissions(ctx.guild.roles[0], send_messages=True)

        await ctx.send(f"🔓The channel {channel.mention} has been unlocked")

    @commands.command(name="slowmode", aliases=['slm'])
    @commands.has_guild_permissions(manage_guild=True)
    async def setdelay(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode in this channel to **{seconds}** seconds!")


def setup(client):
    client.add_cog(Lock_Unlock(client))
