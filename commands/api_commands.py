import requests
import json
import discord
from decouple import config
import urllib


async def covrep(discord, message):
    query = message.content[8:]
    url = "https://coronavirus-map.p.rapidapi.com/v1/spots/week"
    querystring = {"region": query}
    headers = {
        "x-rapidapi-key": config("RAPID_API"),
        "x-rapidapi-host": "coronavirus-map.p.rapidapi.com",
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_data = json.loads(response.text)
        count = 0
        rpt = ""
        for key in json_data["data"]:
            copy = str(key)
            prevnum = 0
            prevnum = int(copy[8:10]) - 1
            prevstr = copy[0:8]
            prev = prevstr + str(prevnum)
            diffcase = (
                json_data["data"][str(key)]["total_cases"]
                - json_data["data"][str(prev)]["total_cases"]
            )
            diffdeath = (
                json_data["data"][str(key)]["deaths"]
                - json_data["data"][prev]["deaths"]
            )
            if diffcase < 0:
                diffcase = 0
            if diffdeath < 0:
                diffdeath = 0
            rpt = (
                str(rpt)
                + str(
                    "\n"
                    + "Covid report of date : "
                    + str(key)
                    + "\n"
                    + "Total No of Cases: "
                    + str(json_data["data"][str(key)]["total_cases"])
                    + " ,"
                    + " Deaths: "
                    + str(json_data["data"][str(key)]["deaths"])
                    + " ,"
                    + " Recoverd: "
                    + str(json_data["data"][str(key)]["recovered"])
                    + " ,"
                    + " Tested: "
                    + str(json_data["data"][str(key)]["tested"])
                )
                + " ,"
                + " New Cases: "
                + str(diffcase)
                + " ,"
                + " New Deaths: "
                + str(diffdeath)
                + "\n"
            )
            count = count + 1
            if count == 5:
                embed = discord.Embed(
                    title="Covid stats of : " + query.capitalize(),
                    description=rpt,
                    color=discord.Color.blue(),
                )

                await message.channel.send(embed=embed)
                break
        await message.add_reaction("\U0001F44d")
    except:
        await message.add_reaction("\U0001F44E")


async def f(discord, message):
    headers = {
        "x-rapidapi-key": config("RAPID_API"),
        "x-rapidapi-host": "numbersapi.p.rapidapi.com",
    }
    querystring = {"json": "true", "fragment": "true"}

    lst = message.content.split()

    if lst[1].find("y") != -1:
        year = lst[2]
        url = "https://numbersapi.p.rapidapi.com/" + year + "/year"

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = json.loads(response.text)
            try:
                await message.channel.send("Date: " + data["date"])
                await message.channel.send(data["text"])
                await message.add_reaction("\U0001f44d")
            except:
                await message.channel.send(data["text"])
                await message.add_reaction("\U0001f44d")
        else:
            await message.add_reaction("\U0001F44E")

    if lst[1].find("m") != -1:
        math = lst[2]
        url = "https://numbersapi.p.rapidapi.com/" + math + "/math"

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = json.loads(response.text)
            await message.channel.send(data["text"])
            await message.add_reaction("\U0001f44d")
        else:
            await message.add_reaction("\U0001F44E")


async def movie(discord, message):
    hold = message.content.find(" ")
    querystring = {
        "query": message.content[(hold + 1) : len(message.content)],
        "page": "1",
    }

    headers = {
        "x-rapidapi-key": config("RAPID_API"),
        "x-rapidapi-host": "advanced-movie-search.p.rapidapi.com",
    }

    result = requests.request(
        "GET",
        "https://advanced-movie-search.p.rapidapi.com/search/movie",
        headers=headers,
        params=querystring,
    )

    data = json.loads(result.text)
    results = data["results"]
    try:
        result_first = results[0]
        await message.add_reaction("\U0001f44d")
    except:
        await message.add_reaction("\U0001F44E")

    await message.channel.send(
        "Original title: "
        + result_first["original_title"]
        + "\nRelease date: "
        + result_first["release_date"]
        + "\nLanguage: "
        + result_first["original_language"]
    )

    await message.channel.send(result_first["poster_path"])
    await message.channel.send("Overview: " + result_first["overview"])


async def song(discord, message):
    hold = message.content.find(" ")
    querystring = {"q": message.content[(hold + 1) : len(message.content)]}

    headers = {
        "x-rapidapi-key": config("RAPID_API"),
        "x-rapidapi-host": "genius.p.rapidapi.com",
    }

    response = requests.request(
        "GET",
        "https://genius.p.rapidapi.com/search",
        headers=headers,
        params=querystring,
    )
    try:
        data = json.loads(response.text)
        response1 = data["response"]
        hits = response1["hits"]

        for i in range(1):
            x = hits[i]
            y = x["result"]
            await message.channel.send(
                "'"
                + y["full_title"]
                + "'"
                + "\nDetails of the song can be found at: "
                + y["url"]
            )
        await message.add_reaction("\U0001f44d")
    except:
        await message.add_reaction("\U0001F44E")


async def math(discord, message):
    hold = message.content.find(" ")
    header = {"content-type": "application/json"}
    querystring = urllib.parse.quote_plus(
        message.content[(hold + 1) : len(message.content)]
    )
    result = requests.get(
        "http://api.mathjs.org/v4/?expr=" + querystring, headers=header
    )
    if result.status_code == 200:
        await message.add_reaction("\U0001f44d")
        await message.channel.send(result.text)
    else:
        await message.add_reaction("\U0001F44E")


async def mean(discord, message):
    word_list = message.content.split()

    if len(word_list) > 2:  # user has more than 2 words as input
        await message.add_reaction("\U0001F44E")
    else:
        word = word_list[1]
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + word

        r = requests.get(url)
        if (
            r.status_code == 200
        ):  # checks status code of response received, 200 is success code
            data = json.loads(r.text)  # dict

            output = ""
            for key in data:
                first_dict = key["phonetics"]
                for phonetics in first_dict:
                    output += "phonetics: " + phonetics["text"] + "\n"

                output += "\n"

                first_dict = key["meanings"]
                for meaning in first_dict:  # list
                    definitions = meaning["partOfSpeech"]
                    output += definitions + " :\n"
                    definitions = meaning["definitions"]  # list

                    i = 1
                    for definition in definitions:  # list
                        define = definition["definition"]
                        output += str(i) + ". " + define + "\n"

                        try:
                            example = definition["example"]
                            output += "example: " + example + "\n"
                        except:
                            pass

                        try:
                            synonyms = definition["synonyms"]
                            output += "synonyms: "
                            for synonym in synonyms:
                                output += synonym + ", "
                            output += "\n"
                        except:
                            pass
                        i += 1
                    output += "\n"

            await message.add_reaction("\U0001F44d")
            embed = discord.Embed(
                title=word, description=output, color=discord.Color.blue()
            )
            await message.channel.send(embed=embed)
        else:
            await message.add_reaction("\U0001F44E")


async def wea(discord, message):
    city_list = message.content.split()
    city = ""
    for i in range(1, len(city_list)):
        city = city + city_list[i] + " "

    newurl = (
        "https://api.openweathermap.org/data/2.5/weather?"
        + "q="
        + city
        + "&appid="
        + config("OPEN_WEATHER_TOKEN")
    )
    response = requests.get(newurl)

    if response.status_code == 200:
        response = response.json()
        weatherrep = response["main"]
        temperature = weatherrep["temp"]
        report = response["weather"]
        humidity = weatherrep["humidity"]
        report_description = str({report[0]["description"]})
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
        await message.channel.send(embed=embed)
        await message.add_reaction("\U0001f44d")
    else:
        await message.add_reaction("\U0001F44E")


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


async def inspire(discord, message):
    try:
        quote = get_quote()
        await message.channel.send(quote)
        await message.add_reaction("\U0001f44d")
    except Exception:
        await message.add_reaction("\U0001F44E")
        await message.channel.send("Quota exhausted :(\nTry again later!")
