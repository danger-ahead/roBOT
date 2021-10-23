import discord
from discord.ext import commands
import wikipedia
from command.database.loader import loader
from command.database.loader import loader


class wikipedia_scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wikipedia_search(self, ctx, *args):
        try:
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
            await ctx.message.add_reaction("\U0001f44d")
            db = loader.db_loaded()
            await db.score_up(ctx, loader.client_loaded())
        except Exception:
            await ctx.message.add_reaction("\U0001f44E")


def setup(bot):
    bot.add_cog(wikipedia_scraper(bot))
