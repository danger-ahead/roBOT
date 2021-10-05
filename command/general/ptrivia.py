import random
import discord
import asyncio
import aiohttp
from discord.ext import commands
from command.database.loader import loader


class Trivia(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def ptrivia(self, ctx):
        url = "https://beta-trivia.bongo.best"
        try:
            async with aiohttp.ClientSession() as session:

                r = await session.get(url)
                r = await r.json()
                r = r[0]
                
                question = r["question"].replace("&quot;", '"').replace("&#039;", "'")
                category = r["category"] if r["category"] is not None else "Unknown"
                correct_answer = (
                    r["correct_answer"].replace("&quot;", '"').replace("&#039;", "'")
                )
                all_answers = r["incorrect_answers"]
                all_answers.append(correct_answer)
                random.shuffle(all_answers)

                channel = ctx.message.channel
                author = ctx.author

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
                    description="Category: "
                    + category
                    + "\n\nOptions:\n"
                    + output
                    + "\nType `correctanswer` for the correct answer.\
                    \nType your answer (not case-sensitive).\
                    You've 60 seconds.",
                    color=discord.Color.blue(),
                )
                msg = await ctx.send(embed=embed)

                def check(m):
                    return m.channel == channel and m.author == author

                all_answers = [x.lower() for x in all_answers]

                try:
                    bot_message = await self.client.wait_for(
                        "message", check=check, timeout=60
                    )
                    if bot_message.content.lower() == correct_answer.lower():
                        await bot_message.add_reaction("\U0001f44d")
                        await bot_message.reply("Correct answer!")
                    elif bot_message.content.lower() == "correctanswer":
                        await bot_message.add_reaction("\U0001f44d")
                        await bot_message.reply(correct_answer)
                    elif bot_message.content.lower() in all_answers:
                        await bot_message.reply(
                            "Wrong answer!\nCorrect answer: " + correct_answer
                        )
                        await bot_message.add_reaction("\U0001f44E")
                    else:
                        await bot_message.reply(
                            "Invalid option chosen!\nCorrect answer: " + correct_answer
                        )
                        await bot_message.add_reaction("\U0001f44E")

                except asyncio.TimeoutError:
                    await msg.reply("Times out\n" + "Correct Answer: " + correct_answer)

                await ctx.message.add_reaction("\U0001f44d")
                db = loader.db_loaded()
                await db.score_up(ctx, loader.client_loaded())

        except:
            await ctx.message.add_reaction("\U0001f44E")
            

def setup(client):
    client.add_cog(Trivia(client))
