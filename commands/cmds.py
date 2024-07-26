from discord.ext import commands
from utils import send_and_delete

command_descriptions = """
**!url or !web** - Get the current URL at which the syllabus is hosted
**!add "book" "author" "series"**: Adds a new book with optional author and series to the syllabus.
**!assign "descriptionOfAssignment"**: Assigns a new assignment for the class."
**!assignment**: Prints the current assignment for the class.
**!cmds**: Displays available bot commands. (you already know this one)
**!columns**: Lists all column names in the syllabus table.
**!complete "bookOrId#"**: Marks an item as complete or incomplete by its name or unique ID.
**!graveyard "minutes"**: Lists all completed items, optionally deletes the message after specified minutes.
**!list_series "series_name"**: Lists all books in a specific series, formatted with authors and order.
~~**!poll "item"**: Initiates a poll for a specific item.~~
**!remove "item"**: Removes an item from the syllabus by name or unique ID.
**!report_bug "description"**: Allows users to report a bug, which then gets inserted into the database.
**!syllabus "minutes"**: Lists all items in the syllabus, optionally deletes the message after specified minutes. Use 0 for infinite time.
**!todo "minutes"**: Lists all incomplete items in the syllabus, optionally deletes the message after specified minutes.
**!update_assignment "descriptionOfAssignment"**: Updates the current assignment for the class.
**!update "bookOrId#" "column" "new_value"**: Updates a specific column of an item in the syllabus.
"""

# The command to display available commands
@commands.command()
async def cmds(ctx):
	await send_and_delete(ctx, command_descriptions)