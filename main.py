import os
import dotenv
import jishaku
import discord
from discord.ext import commands
from command.database.loader import db_load, db_loaded, client_load, client_loaded


# loading env file so that we can use it
dotenv.load_dotenv()


def main():
    db_load()  # loads database
    db = db_loaded()

    client_load()
    client = client_loaded()

    # to load all cogs
    for folder in os.listdir("command"):
        if os.path.exists(os.path.join("command", folder)):
            for filename in os.listdir(f"./command/{folder}"):
                if filename.endswith(".py"):
                    client.load_extension(f"command.{folder}.{filename[:-3]}")

    # loading "jishaku"
    client.load_extension("jishaku")

    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
