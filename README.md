# Teacher Book Club bot
This is my first Discord bot, I made it in python on replit.com. Its purpose is to store a list of books we have/will/want to read in 
our book club. It will post to the book club chat channel upon command to help us keep track of our books.

## [View Discord Demo Here:](https://discord.gg/52vBudgfxk) https://discord.gg/52vBudgfxk

## [View Web Demo Here:](http://34.169.197.3:5000/) http://34.169.197.3:5000/

## Getting Started
To set up the bot, follow these steps:
1. Set up a Discord bot account following [these instructions](https://discordpy.readthedocs.io/en/stable/discord.html).
2. Copy the bot token and add it as a secret with the key `TOKEN` in the "Secrets (Environment variables)" panel on Replit.

## Commands
Prefix all commands with `!`:
- `!add <book> [author] [series]`: Adds a new book with optional author and series to the syllabus.
- `!assign <description> [yyyy-mm-dd]`: Assigns a new assignment for the class. The second argument is an optional due date in yyyy-mm-dd format; if omitted or unparseable it defaults to 2 weeks from today (and any unparseable text is appended to the description).
- `!assignment`: Prints the current assignment for the class.
- `!cmds`: Displays available bot commands.
- `!columns`: Lists all column names in the syllabus table.
- `!complete <identifier>`: Marks a book as complete or incomplete by its name or unique ID.
- `!graveyard [minutes]`: Lists all completed books; optionally auto-deletes after specified minutes.
- `!list_series <series_name>`: Lists all books in a specific series, formatted with authors and order.
- `!remove <identifier>`: Removes a book from the syllabus by name or unique ID.
- `!report_bug <description>`: Reports a bug.
- `!syllabus [minutes]`: Lists all books in the syllabus; optionally auto-deletes after specified minutes. Use 0 for infinite time.
- `!todo [minutes]`: Lists all incomplete books; optionally auto-deletes after specified minutes.
- `!update <identifier> <column> <new_value>`: Updates a specific column of a book in the syllabus.
- `!update_assignment <description>`: Updates the description of the most recent assignment.
- `!url` or `!web`: Prints the current URL for the web application.

## FAQ
If you encounter a `429 Too Many Requests` error, refer to this [Stack Overflow question](https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests).
