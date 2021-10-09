import discord
from stackapi import StackAPI
from discord.ext import commands
import requests
import json

class StackOverflow(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def stack_search(self, ctx, *, args):
        url = f'https://api.stackexchange.com//2.3/search/advanced?page=1&pagesize=1&order=desc&sort=activity&q={args} typeerror&site=stackoverflow'.replace(' ', '+')
        req = requests.get(url)
        data = req.json()
        await ctx.send(data['items'][0]['link'])
        

def setup(client):
    client.add_cog(StackOverflow(client))




