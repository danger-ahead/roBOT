import discord
import json
import requests
from discord.ext import commands

class MAL(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def anime(self, ctx, *args):
        url = requests.get('https://api.jikan.moe/v3/search/anime?q={}&page=1'.format(' '.join(args)))
        data = url.json()
        await ctx.send(data['results'][0]['url'])

    @commands.command()
    async def manga(self, ctx, *args):
        url = requests.get('https://api.jikan.moe/v3/search/manga?q={}&page=1'.format(' '.join(args)))
        data = url.json()
        await ctx.send(data['results'][0]['url'])
        
    
def setup(client):
    client.add_cog(MAL(client))