import os
import dotenv
import discord
import aiohttp
from discord.ext import commands
from command.database.loader import loader


dotenv.load_dotenv()


class Wea(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wea(self, ctx):
        city_list = ctx.message.content.split()
        city = ""
        for i in range(1, len(city_list)):
            city = city + city_list[i] + " "

        newurl = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={str(os.getenv('OPEN_WEATHER_TOKEN'))}"
        async with aiohttp.ClientSession() as session:

            response = await session.get(newurl)
            response = await response.json()

            try:
                weatherrep = response["main"]
                temperature = weatherrep["temp"]
                report = response["weather"]
                humidity = weatherrep["humidity"]
                report_description = str({report[0]["description"]})
                report_ico = report[0][
                    "icon"
                ]  # contains icon id (for more details visit https://openweathermap.org/weather-conditions)
                icon_url = f"https://openweathermap.org/img/wn/{report_ico}@2x.png"  # formats icon id in url
                index = report_description.find("'")
                index2 = report_description.find("'", 2)
                embed = discord.Embed(
                    title="Weather update for :  " + city,
                    description=report_description[(index + 1) : index2]
                    + "\nTemp. is "
                    + str("%.2f" % (temperature - 273))
                    + "℃"
                    + "\nHumidity is "
                    + str(humidity)
                    + "%",
                    color=discord.Color.blue(),
                )
                embed.set_thumbnail(url=icon_url)  # set thumbnail on the embed
                await ctx.send(embed=embed)
                await ctx.message.add_reaction("\U0001f44d")
                db = loader.db_loaded()
                await db.score_up(ctx, loader.client_loaded())

            except:
                await ctx.message.add_reaction("\U0001F44E")


def setup(client):
    client.add_cog(Wea(client))
