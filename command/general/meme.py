import random
import discord
from discord.ext import commands
import aiohttp


class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    def links(self):
        urls = [
            "https://memes.blademaker.tv/api?lang=en",
            "https://memes.blademaker.tv/api/dankmemes",
            "https://memes.blademaker.tv/api/funny",
            "https://memes.blademaker.tv/api/madlad",
            "https://memes.blademaker.tv/api/ComedyCemetery",
            "https://memes.blademaker.tv/api/comedyheaven",
            "https://memes.blademaker.tv/api/technicallythetruth",
            "https://memes.blademaker.tv/api/softwaregore",
            "https://memes.blademaker.tv/api/me_irl",
            "https://memes.blademaker.tv/api/TIHI",
            "https://memes.blademaker.tv/api/facepalm",
            "https://memes.blademaker.tv/api/meme",
            "https://memes.blademaker.tv/api/comics",
            "https://memes.blademaker.tv/api/wholesomememes",
            "https://memes.blademaker.tv/api/goodanimemes",
        ]
        url = random.choice(urls)

        return url

    @commands.command()
    async def meme(self, ctx):
        try:
            # uses https://memes.blademaker.tv/
            url = Meme.links(self)
            async with aiohttp.ClientSession() as session:
                r = await session.get(url)
                r = await r.json()

            title = r["title"]
            sub = r["subreddit"]
            Id = r["id"]
            title_link = title.replace(" ", "_")
            reddit_link = (
                "https://www.reddit.com/r/"
                + sub
                + "/comments/"
                + Id
                + "/"
                + title_link
                + "/"
            )
            embed = discord.Embed(
                title=f"{title}\nsubreddit: {sub}",
                url=reddit_link,
                color=discord.Color.blue(),
            )
            embed.set_image(url=r["image"])

            await ctx.send(embed=embed)
            await ctx.message.add_reaction("\U0001f44d")

        except Exception as e:
            await ctx.send(e)
            # await message.add_reaction("\U0001f44E")


def setup(client):
    client.add_cog(Meme(client))
