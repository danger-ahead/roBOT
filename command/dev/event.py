from discord.ext import commands
import discord

class Start(commands.Cog):
    def __init__(self, client):
        self.client = client

    """
    on_ready is an event; that triggers when u start the bot.
    """
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.client.user} Connected Successfully!")


def setup(client):
    client.add_cog(Start(client))