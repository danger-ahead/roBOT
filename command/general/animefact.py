import os
import airi
import dotenv
from discord.ext import commands

dotenv.load_dotenv()

class AnimeFact(commands.Cog):
    def __init__(self, client):

        self.client = client
        self.airi_client = airi.Client(os.getenv('AIRI'))

    @commands.command(aliases = ['anifact'])
    async def animefact(self, ctx):

        Fact = await self.airi_client.fact()
        fact = Fact.fact

        await ctx.send(fact)
        
def setup(client):
    client.add_cog(AnimeFact(client))