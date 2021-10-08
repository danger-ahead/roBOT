import discord
from stackapi import StackAPI
from discord.ext import commands

class StackOverflow(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def stack_search(self, ctx, *, args):
        SITE = StackAPI('stackoverflow')
        results = SITE.fetch(f'questions/{args}')
        await ctx.send(results['items'][0]['link'])

def setup(client):
    client.add_cog(StackOverflow(client))

