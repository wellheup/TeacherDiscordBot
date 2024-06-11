import os
import discord
import psycopg2.pool
import asyncio
from discord.ext import commands
from replit import db
from keep_alive import keep_alive
from utils import send_and_delete

# Import commands from separate modules
from commands.add import add
from commands.assign import assign
from commands.assignment import assignment
from commands.cmds import cmds
from commands.columns import columns
from commands.complete import complete
from commands.graveyard import graveyard
from commands.list_series import list_series
# from commands.poll import poll
from commands.remove import remove
from commands.report_bug import report_bug
from commands.syllabus import syllabus
from commands.todo import todo
from commands.update_assignment import update_assignment
from commands.update import update

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Register commands with the bot
bot.add_command(add)
bot.add_command(assign)
bot.add_command(assignment)
bot.add_command(cmds)
bot.add_command(columns)
bot.add_command(complete)
bot.add_command(graveyard)
bot.add_command(list_series)
# bot.add_command(poll)
bot.add_command(remove)
bot.add_command(report_bug)
bot.add_command(syllabus)
bot.add_command(todo)
bot.add_command(update_assignment)
bot.add_command(update)

@bot.event
async def on_ready():
	print("I am " + bot.user.name)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	elif bot.user.mentioned_in(message):
		reply = (
			f"I am a keeper of the First House and a servant to the Necrolord Highest, "
			f"and you must call me {bot.user.name}; not due to my own merits of learning, "
			f"but because I stand in the stead of the merciful God Above Death, "
			f"and I live in hope that one day you will call him {bot.user.name}. "
			f"And may I call you then, {message.author.mention}! "
			f"Should you require further instruction type !cmds."
		)
		send_and_delete(message.channel, reply)
	await bot.process_commands(message)

try:
	token = os.getenv("DISCORD_BOT_SECRET") or ""
	if token == "":
		raise Exception("Please add your token to the Secrets pane.")
	keep_alive()
	bot.run(token)

except discord.HTTPException as e:
	if e.status == 429:
		print(
			"The Discord servers denied the connection for making too many requests"
		)
		print(
			"Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
		)
	else:
		raise e

# Todo:
# follow tutorial to see more about bots https://www.youtube.com/watch?v=nW8c7vT6Hl4&list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ&ab_channel=Lucas to make modifications
# add support for the !help command which apparently will give a description automatically...
# add a feature to determine who gets to choose the next book, who chose the last, and who has chosen how many, also a randomizer for who is next in the case of a tie
# add a feature to add a table for each book and then keep a list of or character fan-cast ideas for each book
# add a command to add a book to a season
# add a command to print all of the books in a season
# add a command to print all of the seasons and their books in the order the seasons occurred
# add to add_book to include date added
# add to complete to include date completed
# update the keep_alive.py file to use SQLAlchemy and a database

# sources:
# https://docs.replit.com/tutorials/python/discord-role-bot
# https://docs.replit.com/tutorials/python/build-basic-discord-bot-python
# https://docs.replit.com/hosting/deployments/about-deployments
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.commands
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#commands
# Location for bot in discord: https://discord.com/developers/applications
# hosted: hosted on replit.com
