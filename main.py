import os
import discord
import psycopg2.pool
from discord.ext import commands
from replit import db
from keep_alive import keep_alive
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

pool = psycopg2.pool.SimpleConnectionPool(0,80, os.getenv("DATABASE_URL"))
conn = pool.getconn()
cursor = conn.cursor()

@bot.event
async def on_ready():
	print("I'm a bot")
	print(bot.user)

# function to send message to channel then delete after num minutes
async def send_and_delete(ctx, message, minutes=1):
    if len(message) > 2000:
        message_parts = [message[i:i+2000] for i in range(0, len(message), 2000)]
        for part in message_parts:
            await ctx.send(part, delete_after=minutes*60)
        await ctx.message.add_reaction('👍')
    else:
        await ctx.send(message, delete_after=minutes*60)
        await ctx.message.add_reaction('👍')

# The command to add a new item to the syllabus
@bot.command()
async def add(ctx, book: str, author: str = None, series: str = None):
	# Insert the item to the Syllabus table in the Postgres database
	if author is None:
		cursor.execute("INSERT INTO syllabus (book, added_by, date_added) VALUES (%s, %s, current_date)", (book, ctx.author.name))
	else:
		if series is None:
			cursor.execute("INSERT INTO syllabus (book, author, added_by, date_added) VALUES (%s, %s, %s, current_date)", (book, author, ctx.author.name))
		else:
			cursor.execute("INSERT INTO syllabus (book, author, series, added_by, date_added) VALUES (%s, %s, %s, %s, current_date)", (book, author, series, ctx.author.name))
	conn.commit()
	cursor.close()
	# pool.putconn(conn)
	# pool.closeall()
	
	# Send a message to the chat confirming the addition
	message = f"Added {book} to the syllabus"
	await send_and_delete(ctx, message)


# The commmand to remove an item from the syllabus by name or unique_id
@bot.command()
async def remove(ctx, item):
    if item.isdigit() and int(item) > 0:
        unique_id = int(item)
        cursor.execute("DELETE FROM syllabus WHERE unique_id = %s", (unique_id,))
    else:
        cursor.execute("DELETE FROM syllabus WHERE book = %s", (item,))
    conn.commit()
    cursor.close()

    # Send a message to the chat confirming the removal
    message = f'Removed item "{item}" from the syllabus.'
    await send_and_delete(ctx, message)

@bot.command()
async def complete(ctx, arg):
	if arg.isdigit():
		unique_id = int(arg)
		cursor.execute("SELECT is_completed, date_completed FROM syllabus WHERE unique_id = %s", (unique_id,))
	else:
		book = arg
		cursor.execute("SELECT is_completed, date_completed FROM syllabus WHERE book = %s", (book,))
	
	row = cursor.fetchone()
	
	if row:
		is_completed = row[0]
		date_completed = row[1]
		is_completed = not is_completed
		if is_completed:
			status = "completed"
			if date_completed is None:
				cursor.execute("UPDATE syllabus SET is_completed = %s, date_completed = current_date WHERE unique_id = %s", (is_completed, unique_id))
		else:
			status = "incomplete"
		
		if arg.isdigit():
			if unique_id > 0:
				cursor.execute("UPDATE syllabus SET is_completed = %s WHERE unique_id = %s", (is_completed, unique_id))
				message = f'Marked book {arg} as {status}.'
			else:
				cursor.execute("UPDATE syllabus SET is_completed = %s WHERE book = %s", (is_completed, book))
				message = f'Marked {arg} as {status}.'
		
		conn.commit()

		await send_and_delete(ctx, message)
	else:
		message = "No matching item found."
		await send_and_delete(ctx, message)
		
# The command to list all the items in the syllabus
@bot.command()
async def syllabus(ctx, minutes: int = 5):
	cursor.execute("SELECT book, author, series, num_in_series, unique_id, is_completed FROM syllabus ORDER BY author, series, num_in_series")
	rows = cursor.fetchall()
	currentAuthor = ''
	currentSeries = ''
	syllabus_str = '**The current syllabus is as follows: **\n'

	for row in rows:
		# syllabus_str += f'**{row[0]}** by **{row[1]}** ({row[2]}) - {row[3]}/{row[4]} - {row[5]}\n' 
		book = f'*{row[0]}*'
		author = row[1]
		series = row[2]
		num_in_series = row[3]
		if row[5] == 1:
			book += ' ✅'
		if author != currentAuthor:
			syllabus_str += f'{author}\n'
			currentAuthor = author
		if series == '':
			currentSeries = series
			syllabus_str += f'- {book} ({row[4]})\n'
		elif series != currentSeries:
			currentSeries = series
			syllabus_str += f'- {currentSeries}\n'
			syllabus_str += f'  - {book} ({row[4]})\n'
		else:
			syllabus_str += f'  - {book} ({row[4]})\n'

	message = syllabus_str
	if minutes == 0:
		await ctx.send(message)
	else:
		await send_and_delete(ctx, message, minutes)

# The command to list all the incomplete items in the syllabus
@bot.command()
async def todo(ctx, minutes: int = 5):
	cursor.execute("SELECT book, author, series, num_in_series, unique_id, is_completed FROM syllabus WHERE is_completed = false ORDER BY author, series, num_in_series")
	rows = cursor.fetchall()
	currentAuthor = ''
	currentSeries = ''
	syllabus_str = '**The current syllabus is as follows: **\n'

	for row in rows:
		# syllabus_str += f'**{row[0]}** by **{row[1]}** ({row[2]}) - {row[3]}/{row[4]} - {row[5]}\n' 
		book = f'*{row[0]}*'
		author = row[1]
		series = row[2]
		num_in_series = row[3]
		if row[5] == 1:
			book += ' ✅'
		if author != currentAuthor:
			syllabus_str += f'{author}\n'
			currentAuthor = author
		if series == '':
			currentSeries = series
			syllabus_str += f'- {book} ({row[4]})\n'
		elif series != currentSeries:
			currentSeries = series
			syllabus_str += f'- {currentSeries}\n'
			syllabus_str += f'  - {book} ({row[4]})\n'
		else:
			syllabus_str += f'  - {book} ({row[4]})\n'

	message = syllabus_str
	if minutes == 0:
		await ctx.send(message)
	else:
		await send_and_delete(ctx, message, minutes)

@bot.command()
async def poll(ctx, item):
	await ctx.message.add_reaction('👍')
	if item.isdigit() and int(item) > 0:
		unique_id = int(item)
		cursor.execute("SELECT unique_id FROM syllabus WHERE unique_id = %s", (unique_id,))
	else:
		book = item
		cursor.execute("SELECT book FROM syllabus WHERE book = %s", (book,))

	row = cursor.fetchone()

	if row:
		book_title = row[0]
		poll_message = await ctx.send(f"Would you like to read '{book_title}'?\n '💯' to end poll.")
		await poll_message.add_reaction('👍')
		await poll_message.add_reaction('👎')
		await poll_message.add_reaction('💯')

		def check(reaction, user):
			return str(reaction.emoji) == '💯' and user != bot.user

		async def postResults():
			# reaction_dict = poll_message.reactions
			reaction_dict = discord.utils.get(bot.cached_messages, id=poll_message.id).reactions
			up_votes = 0
			down_votes = 0
			for reaction in reaction_dict:
				if str(reaction.emoji) == '👍':
					up_votes = reaction.count - 1  # Subtract 1 to exclude bot's reaction
				elif str(reaction.emoji) == '👎':
					down_votes = reaction.count - 1  # Subtract 1 to exclude bot's reaction

			cursor.execute("UPDATE syllabus SET up_votes = %s, down_votes = %s WHERE book = %s", (up_votes, down_votes, book_title))
			conn.commit()

			result_message = await ctx.send(f"Up Votes: {up_votes}, Down Votes: {down_votes}")
			await result_message.add_reaction('💯')
			await poll_message.delete()
			try:
				await bot.wait_for('reaction_add', timeout=20, check=check)
				await result_message.delete()
			except asyncio.TimeoutError:
				await result_message.delete()


		try:
			await bot.wait_for('reaction_add', timeout=20, check=check)
			await postResults()
		except asyncio.TimeoutError:
			await postResults()
	else:
		message = "No matching item found."
		await send_and_delete(ctx, message)

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

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  elif bot.user.mentioned_in(message):
    await message.channel.send(
      f"I am a keeper of the First House and a servant to the Necrolord Highest, and you must call me {bot.user.name}; not due to my own merits of learning, but because I stand in the stead of the merciful God Above Death, and I live in hope that one day you will call him {bot.user.name}. And may I call you then, {message.author.mention}! "
    )
  await bot.process_commands(message)

try:
	token = os.getenv("DISCORD_BOT_SECRET") or ""
	if token == "":
		raise Exception("Please add your token to the Secrets pane.")
	keep_alive()
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
# add a feature to determine who gets to chooose the next book, who chose the last, and who has chosen how many, also a randomizer for who is next in the case of a tie

# sources:
# https://docs.replit.com/tutorials/python/discord-role-bot
# https://docs.replit.com/tutorials/python/build-basic-discord-bot-python
# https://docs.replit.com/hosting/deployments/about-deployments
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.commands
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#commands
# hosting: https://billing.sparkedhost.com/clientarea.php