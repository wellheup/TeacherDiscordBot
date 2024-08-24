import threading
import os
from keep_alive import keep_alive
from replit import db
from utils import daily_update_url

# Web App
from my_flask_app import app as flask_app
def run_flask():
	daily_update_url()
	port = 80 if os.getenv('REPLIT_DEPLOYMENT') == '1' else 5000
	flask_app.run(host='0.0.0.0', port=port)

# Discord bot 
import discord
from discord.ext import commands
from utils import send_and_delete

def run_discord_bot():
	daily_update_url()
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
	from commands.url import url
	
	intents = discord.Intents.default()
	intents.message_content = True
	prefix = '!' if os.getenv('REPLIT_DEPLOYMENT') == '1' else '.'
	bot = commands.Bot(command_prefix=prefix, intents=intents)
	
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
	bot.add_command(url)
	
	@bot.event
	async def on_ready():
		print(f"I am {bot.user.name}. The live url is:\nhttps://teacher-phillipmm.replit.app/?url_suffix={db.get('url_suffix', '')}\n")
		
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
		token = os.getenv("DISCORD_BOT_SECRET")
		if not token:
			raise Exception("Please add your token to the Secrets pane.")
		bot.run(token)
		keep_alive()
	
	except discord.HTTPException as e:
		if e.status == 429:
			print("The Discord servers denied the connection for making too many requests")
			print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
		else:
			raise e

if __name__ == '__main__':
	flask_thread = threading.Thread(target=run_flask)
	discord_thread = threading.Thread(target=run_discord_bot)

	flask_thread.start()
	discord_thread.start()
	flask_thread.join()
	discord_thread.join()

# TODO:
# follow tutorial to see more about bots https://www.youtube.com/watch?v=nW8c7vT6Hl4&list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ&ab_channel=Lucas to make modifications

# sources:
# https://docs.replit.com/tutorials/python/discord-role-bot
# https://docs.replit.com/tutorials/python/build-basic-discord-bot-python
# https://docs.replit.com/hosting/deployments/about-deployments
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.commands
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#commands
# Location for bot in discord: https://discord.com/developers/my_flask_apps
# hosted: hosted on replit.com
