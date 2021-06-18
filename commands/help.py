"""
Module containing the function for _help command.
"""


async def help(discord, message):
    cmd = message.content.split()

    try:
        # Administrator Commands
        if cmd[1] == "configure":
            embed = discord.Embed(
                title="configure",
                description="Configures roBOT to use a particular channel for admin commands",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$configure`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "deconfigure":
            embed = discord.Embed(
                title="deconfigure",
                description="Deconfigures roBOT from using the configured channel for admin commands",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$deconfigure`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "configconfess":
            embed = discord.Embed(
                title="configconfess",
                description="Configures roBOT to use a particular channel for the confessions",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$configconfess`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "deconfigconfess":
            embed = discord.Embed(
                title="deconfigconfess",
                description="Deconfigures roBOT from using the configured confession channel for the confessions",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$deconfigconfess`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "kick":
            embed = discord.Embed(
                title="kick",
                description="roBOT kicks the mentioned user",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$kick @< user >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "mute":
            embed = discord.Embed(
                title="mute",
                description="roBOT mutes the mentioned user",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$mute @< user >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "unmute":
            embed = discord.Embed(
                title="unmute",
                description="roBOT unmutes the mentioned user",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$unmute @< user >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "moderation":
            embed = discord.Embed(
                title="moderation",
                description="Instructs roBOT to activate chat moderation on the server",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$moderation`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "rank":
            embed = discord.Embed(
                title="rank",
                description="Tells the current friendship level of roBOT with the user",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$rank`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "leave":
            embed = discord.Embed(
                title="leave",
                description="Instructs roBOT to leave the server (works only in the channel configured with `$configure` command)",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$leave`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "clean":
            embed = discord.Embed(
                title="clean",
                description="roBOT deletes the previous 100 chats from the channel",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`$clean`")
            await message.channel.send(embed=embed)

        # General Commands
        elif cmd[1] == "hi":
            embed = discord.Embed(
                title="hi",
                description="Provides the user with a link to find roBOT's commands",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_hi`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "contribute":
            embed = discord.Embed(
                title="contribute",
                description="Provides the user with a link to roBOT's source code",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_contribute`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "mean":
            embed = discord.Embed(
                title="mean",
                description="Finds the meaning of the word",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_mean < word >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "math":
            embed = discord.Embed(
                title="math",
                description="Solves the Math Problem",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_math < problem >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "f" and cmd[2] == "m":
            embed = discord.Embed(
                title="f m",
                description="Tells an interesting fact about the number",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_f m < number >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "f" and cmd[2] == "y":
            embed = discord.Embed(
                title="f y",
                description="Tells an interesting fact about the year",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_f y < year>`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "joke":
            embed = discord.Embed(
                title="joke",
                description="Tells a joke",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_joke`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "wea":
            embed = discord.Embed(
                title="wea",
                description="Tells the current weather situations of the city",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_wea < city, country code >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "wiki":
            embed = discord.Embed(
                title="wiki",
                description="Searches the Wikipedia for the query",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_wiki < query >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "search":
            embed = discord.Embed(
                title="search",
                description="Searches DuckDuckGo for the query",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_search < query >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "movie":
            embed = discord.Embed(
                title="movie",
                description="Tells the details of the movie",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_movie < movie >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "song":
            embed = discord.Embed(
                title="song",
                description="Tells the details of the song or finds the most famous song of the artist",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_song < song or artist >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "confess":
            embed = discord.Embed(
                title="confess",
                description="roBOT deletes the user's confession message and forwards the confession message to configured confession channel anonymously",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_confess < confession >`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "quiz":
            embed = discord.Embed(
                title="quiz",
                description="Starts quiz",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_quiz`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "qstop":
            embed = discord.Embed(
                title="qstop",
                description="Stops an ongoing quiz",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_qstop`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "scores":
            embed = discord.Embed(
                title="scores",
                description="Tells the current scores of the quiz participants",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_scores`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "next":
            embed = discord.Embed(
                title="next",
                description="Skips to the next question in quiz",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_next`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "reset":
            embed = discord.Embed(
                title="reset",
                description="Resets the quiz",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_reset`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "rolldice":
            embed = discord.Embed(
                title="rolldice",
                description="Rolls a dice",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_rolldice`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "tosscoin":
            embed = discord.Embed(
                title="tosscoin",
                description="Tosses a coin",
                color=discord.Color.blue(),
            )
            embed.add_field(name="**Syntax**", value="`_tosscoin`")
            await message.channel.send(embed=embed)

        elif cmd[1] == "poll":
            embed = discord.Embed(
                title="poll",
                description="Creates a poll and the users vote by reacting (clicking) on the respective choice's emoji",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="**Syntax**",
                value="`_poll < topic >,,< choice1 >,,< choice2 >,,...,,< upto choice9 >,,< poll duration >`",
            )
            await message.channel.send(embed=embed)

    except:
        embed = discord.Embed(
            title="HELP",
            description="Use `_help <command name>` to find details about the command",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="**Administrator Commands**",
            value="configure, deconfigure, configconfess, deconfigconfess, kick, mute, unmute, moderation, rank, leave, clean",
            inline=False,
        )
        embed.add_field(
            name="**General Commands**",
            value="hi, contribute, mean, math, f m, f y, joke, wea, wiki, search, movie, song, confess",
            inline=False,
        )
        embed.add_field(
            name="**Quiz Commands**",
            value="quiz, qstop, scores, next, reset",
            inline=False,
        )
        embed.add_field(
            name="**Game Commands**",
            value="rolldice, tosscoin, poll",
            inline=False,
        )
        await message.channel.send(embed=embed)
