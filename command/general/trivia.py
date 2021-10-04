import asyncio
import discord
import requests
import random
from discord.ext import commands


class Ptrivia(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def trivia(self, ctx):
        url = "https://beta-trivia.bongo.best"
        try:
            r = requests.get(url).json()[0]

            question = r["question"].replace("&quot;", '"').replace("&#039;", "'")
            category = r["category"] if r["category"] is not None else "Unknown"
            correct_answer = (
                r["correct_answer"].replace("&quot;", '"').replace("&#039;", "'")
            )
            all_answers = r["incorrect_answers"]
            all_answers.append(correct_answer)
            random.shuffle(all_answers)

            embed = discord.Embed(
                title=question,
                description=f"Category: {category}\n\nOptions in 10 seconds...",
                color=discord.Color.blue(),
            )
            msg = await ctx.send(embed=embed)

            await asyncio.sleep(10)

            i = 1
            output = ""
            for answers in all_answers:
                output += (
                    str(i)
                    + ". "
                    + answers.replace("&quot;", '"').replace("&#039;", "'")
                    + "\n"
                )
                i += 1

            embed = discord.Embed(
                title=question,
                description=f"Category: {category}\n\n"
                + "Options:\n"
                + output
                + "\nCorrect answer in 10 seconds...",
                color=discord.Color.blue(),
            )
            await msg.edit(embed=embed)

            await asyncio.sleep(10)

            embed = discord.Embed(
                title=question,
                description=f"Category: {category}\n\n"
                + "Correct answer: "
                + correct_answer,
                color=discord.Color.blue(),
            )
            await msg.edit(embed=embed)
            await ctx.message.add_reaction("\U0001f44d")

        except Exception:
            await ctx.message.add_reaction("\U0001f44E")


def setup(client):
    client.add_cog(Ptrivia(client))
