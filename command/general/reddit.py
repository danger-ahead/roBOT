from discord.ext import commands
import asyncpraw
from dotenv import load_dotenv
import os
import discord


load_dotenv()

reddit = asyncpraw.Reddit(
    #add in your client id and client secret and user agent from your reddit application panel 
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
    user_agent="DuckyBot"
)

class reddit_scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="fetch memes from any subreddit", pass_context = True)
    async def reddit_meme(self, ctx, *args):
        submission = await reddit.subreddit('{}'.format(' '.join(args))).Hot()
        em = discord.Embed(title=submission.title, description=submission.selftext[:2048], url = submission.url, color=0xFF4301)        
        em.set_image(url=submission.url)
        await ctx.send(embed = em)
        await ctx.message.delete()

   

def setup(bot):
        bot.add_cog(reddit_scraper(bot))