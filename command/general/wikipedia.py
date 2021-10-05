import discord
from discord.ext import commands
import wikipedia


class wikipedia_scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wikipedia_search(self, ctx, *args):
        result = wikipedia.page("{}".format(" ".join(args)))
        em = discord.Embed(
            title=result.title, description=result.content[:2048], color=0xFFFFFF
        )
        em.add_field(
            name="Page Link",
            value=f'https://en.wikipedia.org/wiki/{result.title.replace(" ", "_")}',
            inline=False,
        )
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(wikipedia_scraper(bot))
