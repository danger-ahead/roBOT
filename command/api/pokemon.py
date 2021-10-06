import discord
import json
import aiohttp
from discord.ext import commands


class Pokemon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pokedex(self, ctx, args):
        async with aiohttp.ClientSession() as session:
            url = await session.get(
                "https://pokeapi.co/api/v2/pokemon/{}".format(args)
            )
            data = await url.json()

        em = discord.Embed(title=data["name"])
        em.set_image(url=data["sprites"]["front_default"])
        em.add_field(name="ID", value=data["id"])
        em.add_field(name="Base XP", value=data["base_experience"])
        em.add_field(name="Height", value=data["height"])
        em.add_field(name="HP", value=data["stats"][0]["base_stat"])
        em.add_field(name="Attack", value=data["stats"][1]["base_stat"])
        em.add_field(name="Defense", value=data["stats"][2]["base_stat"])
        em.add_field(name="SP.Atk", value=data["stats"][3]["base_stat"])
        em.add_field(name="SP.Def", value=data["stats"][4]["base_stat"])
        em.add_field(name="Speed", value=data["stats"][5]["base_stat"])

        for i in range(0, 2):
            em.add_field(
                name="Ability",
                value=data["abilities"][i]["ability"]["name"]
            )

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Pokemon(client))
