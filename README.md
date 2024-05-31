# Teacher Book Club bot
This is my first Discord bot, I made it in python on replit.com. Its purpose is to store a list of books we have/will/want to read in 
our book club. It will post to the book club chat channel upon command to help us keep track of our books.

## Getting Started
To get set up, you'll need to follow [these bot account setup instructions](https://discordpy.readthedocs.io/en/stable/discord.html),
and then copy the token for your bot and added it as a secret with the key of `TOKEN` in the "Secrets (Environment variables)" panel.

## Commands
To use commands, first type an !
```
**!add <book> [author] [series]	**: Adds a new book with optional author and series to the syllabus.
**!remove <item>**: Removes an item from the syllabus by name or unique ID.
**!complete <identifier>**: Marks an item as complete or incomplete by its name or unique ID.
**!syllabus [minutes]**: Lists all items in the syllabus, optionally deletes the message after specified minutes. Use 0 for infinite time.
**!todo [minutes]**: Lists all incomplete items in the syllabus, optionally deletes the message after specified minutes.
**!graveyard [minutes]**: Lists all completed items, optionally deletes the message after specified minutes.
**!poll <item>**: Initiates a poll for a specific item.
**!update <identifier> <column> <new_value>**: Updates a specific column of an item in the syllabus.
**!list_series <series_name>**: Lists all books in a specific series, formatted with authors and order.
**!columns**: Lists all column names in the syllabus table.
**!cmds**: Displays available bot commands. (you already know this one)
**!report_bug <description>**: Allows users to report a bug, which then gets inserted into the database.
```


## FAQ
If you get the following error message while trying to start the server: `429 Too Many Requests` (accompanied by a lot of HTML code), 
try the advice given in this Stackoverflow question:
https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests
