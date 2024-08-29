# Teacher Book Club bot
This is my first Discord bot, I made it in python on replit.com. Its purpose is to store a list of books we have/will/want to read in 
our book club. It will post to the book club chat channel upon command to help us keep track of our books.

##[View Discord Demo Here:](https://discord.gg/52vBudgfxk) https://discord.gg/52vBudgfxk
##[View Web Demo Here:](https://teacher-phillipmm.replit.app/#) https://teacher-phillipmm.replit.app/#

## Getting Started
To set up the bot, follow these steps:
1. Set up a Discord bot account following [these instructions](https://discordpy.readthedocs.io/en/stable/discord.html).
2. Copy the bot token and add it as a secret with the key `TOKEN` in the "Secrets (Environment variables)" panel on Replit.

## Commands
Prefix all commands with `!`:
- `!add <book> [author] [series]`: Adds a new book with optional author and series.
- `!remove <identifier>`: Removes a book by name or unique ID.
- `!complete <identifier>`: Marks a book as complete or incomplete by its name or unique ID.
- `!syllabus [minutes]`: Lists all books in the syllabus; optionally auto-deletes after specified minutes.
- `!todo [minutes]`: Lists all incomplete books; optionally auto-deletes after specified minutes.
- `!graveyard [minutes]`: Lists all completed books; optionally auto-deletes after specified minutes.
- `!poll <book>`: Initiates a poll for a specific book.
- `!update <identifier> <column> <new_value>`: Updates a specific column of a book in the syllabus.
- `!list_series <series_name>`: Lists all books in a specific series.
- `!columns`: Lists all column names in the syllabus table.
- `!cmds`: Displays available bot commands.
- `!report_bug <description>`: Reports a bug.
- `!web` or `!url`: will print the current url for the web application in a live deployment

## FAQ
If you encounter a `429 Too Many Requests` error, refer to this [Stack Overflow question](https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests).
