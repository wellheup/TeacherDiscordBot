import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', help_command=CustomHelpCommand(), intents=intents)

@bot.event
async def on_ready():
	print("I'm a bot")
	print(bot.user)

# function to send message to channel then delete after num minutes
async def send_and_delete(ctx, message, minutes = 1):
	await ctx.send(message, delete_after = minutes * 60)
	await ctx.message.add_reaction('👍')

# The command to add a new item to the syllabus
@bot.command()
async def add(ctx, *args):
	# Join the arguments into a single string
	item = ' '.join(args)

	# Add the item to the syllabus
	# syllabus.append(item) # local var instead of .txt file
	with open('syllabus.txt', 'a') as f:
		f.write('\n' + item.strip())
		f.close()

	# Send a message to the chat confirming the addition
	message = f"Added {item} to the syllabus"
	await send_and_delete(ctx, message)

# The commmand to remove an item from the syllabus by name
@bot.command()
async def remove(ctx, *args):
	# Join the arguments into a single string
	item = ' '.join(args)
	# Remove item from syllabus
	with open('syllabus.txt', 'r') as f:
		lines = f.readlines()
		f.close()
	with open('syllabus.txt', 'w') as f:
		for line in lines:
			if item not in line and line.strip():
				f.write(line)
		f.close()
	
	# Send a message to the chat confirming the removal
	message = f'Removed "{item}" from the syllabus.'
	await send_and_delete(ctx, message)

# The commmand to remove an item from the syllabus by index
@bot.command()
async def removeNum(ctx, index: int):
	# adjust indexing to start at 1
	index -=1

	# Get the item at the specified index
	with open('syllabus.txt', 'r') as f:
		lines = f.readlines()
		f.close()
		
	# Check if the index is valid
	if index < 0 or index >= len(lines):
		await ctx.send('Invalid index.')
		return

	# Remove the item from the syllabus
	with open('syllabus.txt', 'w') as f:
		for line in lines:
			if line.strip() != lines[index].strip():
				f.write(line)
		f.close()
	# Send a message to the chat confirming the removal
	message = f'Removed {lines[index].strip()} from the syllabus.'
	await send_and_delete(ctx, message)

# The command to update the font of an item to strikethrough by text
@bot.command()
async def strike(ctx, *args):
	# Join the arguments into a single string
	item = ' '.join(args)
	# Open the syllabus.txt file and read its contents into a list
	with open('syllabus.txt', 'r') as f:
		lines = f.readlines()
		f.close()

	# Update the item in the list
	with open('syllabus.txt', 'w') as f:
		for line in lines:
			if line.strip() != item:
				f.write(line)
			elif '~~' in line:
				f.write(item)
			else:
				f.write('~~' + item.strip() + '~~' + '\n')
		f.close()	

	# Send a message to the chat confirming the update
	message = f'Updated "{item}" to strikethrough.'
	await send_and_delete(ctx, message)

# The command to update the font of an item to strikethrough by index
@bot.command()
async def strikeNum(ctx, index: int):
	# adjust indexing to start at 1
	index -=1
	
	# Open the syllabus.txt file and read its contents into a list
	with open('syllabus.txt', 'r') as f:
		lines = f.readlines()
		f.close()
		
	# Check if the index is valid
	if index < 0 or index >= len(lines):
		await ctx.send('Invalid index.')
		return

	# Update the item in the list
	with open('syllabus.txt', 'w') as f:
		for line in lines:
			if line.strip() != lines[index].strip():
				f.write(line)
			elif '~~' in line:
				f.write(line.replace('~~', '', 2))
			else:
				f.write('~~' + line.strip() + '~~' + '\n')
		f.close()	
		
	# Send a message to the chat confirming the update
	message = f'Updated item {index+1}, "{lines[index]}" to strikethrough.'
	await send_and_delete(ctx, message)

# The command to update the font of an item to bold by text
@bot.command()
async def bold(ctx, *args):
	# Join the arguments into a single string
	item = ' '.join(args)
	# Open the syllabus.txt file and read its contents into a list
	with open('syllabus.txt', 'r') as f:
		lines = f.readlines()
		f.close()

	# Update the item in the list
	with open('syllabus.txt', 'w') as f:
		for line in lines:
			if line.strip() != item:
				f.write(line)
			elif '**' in line:
				f.write(item)
			else:
				f.write('**' + item.strip() + '**' + '\n')
		f.close()	

	# Send a message to the chat confirming the update
	message = f'Updated "{item}" to bold.'
	await send_and_delete(ctx, message)

# The command to update the font of an item to bold by index
@bot.command()
async def boldNum(ctx, index: int):
	# adjust indexing to start at 1
	index -=1

	# Open the syllabus.txt file and read its contents into a list
	with open('syllabus.txt', 'r') as f:
		lines = f.readlines()
		f.close()

	# Check if the index is valid
	if index < 0 or index >= len(lines):
		await ctx.send('Invalid index.')
		return

	# Update the item in the list
	with open('syllabus.txt', 'w') as f:
		for line in lines:
			if line.strip() != lines[index].strip():
				f.write(line)
			elif '**' in line:
				f.write(line.replace('**', '', 2))
			else:
				f.write('**' + line.strip() + '**' + '\n')
		f.close()	

	# Send a message to the chat confirming the update
	message = f'Updated item {index+1}, "{lines[index]}" to bold.'
	await send_and_delete(ctx, message)

# The command to post the syllabus in the chat
@bot.command()
async def syllabus(ctx, minutes: int = 5):
	# Open the syllabus.txt file and read its contents into a list
	with open('syllabus.txt', 'r') as f:
		syllabus = f.readlines()
		f.close()

	# Create a string with the syllabus of syllabus
	syllabus_str = '**The current syllabus is as follows: **\n'
	syllabus_str += '\n'.join([f'{index+1}. {item.strip()}' for index, item in enumerate(syllabus)])

	# Send the syllabus to the chat
	message = syllabus_str
	if minutes == 0:
		await ctx.send(message)
	else:
		await send_and_delete(ctx, message, minutes)

# The command to display available commands
@bot.command()
async def cmds(ctx):
	# Open the syllabus.txt file and read its contents into a list
	with open('cmds.txt', 'r') as f:
		syllabus = f.readlines()
		f.close()

	# Create a string with the syllabus of syllabus
	help_str = '\n'.join([f'{item.strip()}' for index, item in enumerate(syllabus)])

	# Send the commands to the chat
	message = f'\n```{help_str}```'
	await send_and_delete(ctx, message)

# The command to add bugs to the bug list
@bot.command()
async def bug(ctx, *args):
	# Join the arguments into a single string
	item = ' '.join(args)

	with open('bugs.txt', 'a') as f:
		f.write(item + '\n')
		f.close()

	# Send a message to the chat confirming the addition
	message = f"Added {item} to the bug list"
	await send_and_delete(ctx, message)

try:
	token = os.getenv("DISCORD_BOT_SECRET") or ""
	if token == "":
		raise Exception("Please add your token to the Secrets pane.")
	# Run the bot
	bot.run(token)

except discord.HTTPException as e:
	if e.status == 429:
		print(
			"The Discord servers denied the connection for making too many requests"
		)
		print(
			"Get help from https://stackoverflow.com/questions/66724687/"+
			"in-discord-py-how-to-solve-the-error-for-toomanyrequests"
		)
	else:
		raise e


# Todo
# add a graveyard function
# add a support for editing a line in place, rather than deleting and re-adding
# add a function for viewing just a series by index or text
# add support for subgroups (book series or authors)
# add support for the !help command which apparently will give a description automatically...
# see what happens if all of the @bots are changed to @client
# add a command that triggers when someone calls @botName where it will introduce itself and share its commands
# add a feature to say who added a book to syllabus		

# sources:
# https://docs.replit.com/tutorials/python/discord-role-bot
# https://docs.replit.com/tutorials/python/build-basic-discord-bot-python
# https://docs.replit.com/hosting/deployments/about-deployments
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.commands
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#commands
# hosting: https://billing.sparkedhost.com/clientarea.php