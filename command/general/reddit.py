import os
import discord
import asyncpraw
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


class reddit_scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="fetch memes from any subreddit")
    async def reddit(self, ctx, subreddit : str = 'meme', limit = 25):
        # adding this limitation below to prevent api abuse.
        if limit > 100:
            limit = 100
            
        reddit = asyncpraw.Reddit(
            # add in your client id and client secret in .env file
            client_id = os.getenv('CLIENT_ID'),
            client_secret = os.getenv("CLIENT_SECRET"),
            user_agent="roBOT",
        )

        try:
            subreddit = await reddit.subreddit(subreddit)
            submission = random.choice([meme async for meme in subreddit.hot(limit = limit)])
            
            em = discord.Embed(
                title=submission.title,
                description=submission.selftext[:2048],
                url=submission.url,
                color=0xFF4301,
            )
            em.set_image(url=submission.url)
            await ctx.send(embed=em)
            await ctx.message.add_reaction("👍")

        except Exception as e:
            await ctx.send(e)
            await ctx.message.add_reaction("👎")

        finally:
            await reddit.close()


def setup(bot):
    bot.add_cog(reddit_scraper(bot))
