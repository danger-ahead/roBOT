import os


class Moderator:
    """
    Class for all the moderation functions
    """

    def __init__(self):
        # relative path to scripts directory
        os.chdir("commands/scripts")
        # opens, reads and adds the contents of the file to a list
        file = open(
            "moderate_words.txt", "r"
        )  # add words of your choice in moderate_words
        self.read_file = file.read().split()
        # changes back to project directory`
        os.chdir("..")
        print("Loaded: scripts/moderate_words.txt")
        print("Running: Moderator module [moderator.py]\n")

    async def check(self, message):
        message_word_list = message.content.lower().split(" ")

        for word in message_word_list:
            # searches for each word from message
            if word in self.read_file:
                await message.reply("You're being warned!")
                break
