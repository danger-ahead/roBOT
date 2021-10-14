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

def setup(client):
    client.add_cog(Lock_Unlock(client))
