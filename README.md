# roBOT

![](https://img.shields.io/github/stars/danger-ahead/roBOT) ![](https://img.shields.io/github/forks/danger-ahead/roBOT) ![](https://img.shields.io/github/issues/danger-ahead/roBOT)

## Prerequisites
- The bot uses [Numbers](https://rapidapi.com/divad12/api/numbers-1) from [RapidAPI](https://rapidapi.com/marketplace) for displaying year and math facts.
- The bot uses [DuckDuckGo](https://duckduckgo.com/) for fetching search results

- Python Packages required:
	- [discord.py](https://pypi.org/project/discord.py/)
	- [duckduckgo-search](https://pypi.org/project/duckduckgo-search/)
	- [requests](https://pypi.org/project/requests/)
	- [python-decouple](https://pypi.org/project/python-decouple/)

## Installation
- Head over to this [freecodecamp tutorial](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)
- In the .env  file, paste the required keys as:
	` TOKEN=YOUR_TOKEN` (replace 'YOUR_TOKEN' with your token)
	`NUMBERS_API=YOUR_API_KEY` (replace 'YOUR_API_KEY' with your API key)

## Working
#### For receiving year and math facts:
`_f y`followed by the year
`_f m`followed by the number
#### For performing a search
`_search`followed by the search phrase
#### For finding the meaning of a word
`_mean`followed by the word