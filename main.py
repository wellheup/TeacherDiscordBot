import os
import discord
import psycopg2.pool
import asyncio
from discord.ext import commands
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

pool = psycopg2.pool.SimpleConnectionPool(0, 80, os.getenv("DATABASE_URL"))
conn = pool.getconn()
cursor = conn.cursor()

@bot.event
async def on_ready():
	print("I am " +bot.user.name)

# function to send message to channel then delete after num minutes
async def send_and_delete(ctx, message, minutes=5):
	allowed_mentions = discord.AllowedMentions.none()  # Prevent mentions
	if len(message) > 2000:
		message_parts = []
		current_part = ""
		for line in message.split('\n'):
			if line.startswith('**'):
				if current_part:
					message_parts.append(current_part)
					current_part = ""
			current_part += f"{line}\n"
		message_parts.append(current_part)
		if ctx.channel.name == 'office-hours':
			await ctx.message.add_reaction('👍')
			for part in message_parts:
				await ctx.send("@silent " + part, allowed_mentions=allowed_mentions)
		else:
			await ctx.message.delete()
			for part in message_parts:
				await ctx.send("@silent " + part, delete_after=minutes * 60, allowed_mentions=allowed_mentions)
	else:
		if ctx.channel.name == 'office-hours':
			await ctx.send("@silent " + message, allowed_mentions=allowed_mentions)
			await ctx.message.add_reaction('👍')
		else:
			await ctx.message.delete()
			await ctx.send("@silent " + message, delete_after=minutes * 60, allowed_mentions=allowed_mentions)

command_descriptions = """
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
"""

# The command to add a new item to the syllabus
@bot.command()
async def add(ctx, book: str, author: str = None, series: str = None):
	conn = pool.getconn()
	cursor = conn.cursor()
	
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
	
	# Send a message to the chat confirming the addition
	message = f"Added {book} to the syllabus"
	await send_and_delete(ctx, message)

# The commmand to remove an item from the syllabus by name or unique_id
@bot.command()
async def remove(ctx, item):
	conn = pool.getconn()
	cursor = conn.cursor()
	
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
	conn = pool.getconn()
	cursor = conn.cursor()
	
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
	conn = pool.getconn()
	cursor = conn.cursor()
	
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
			syllabus_str += f'**{author}**\n'
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
	conn = pool.getconn()
	cursor = conn.cursor()
	
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
			syllabus_str += f'**{author}**\n'
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
async def graveyard(ctx, minutes: int = 5):
	conn = pool.getconn()
	cursor = conn.cursor()
	
	cursor.execute("SELECT book, author, series, num_in_series, unique_id, is_completed FROM syllabus WHERE is_completed = true ORDER BY author, series, num_in_series")
	rows = cursor.fetchall()
	currentAuthor = ''
	currentSeries = ''
	syllabus_str = '**The following assignments have already been completed: **\n'

	for row in rows:
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
	conn = pool.getconn()
	cursor = conn.cursor()
	
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

@bot.command()
async def update(ctx, identifier, column, new_value):
	conn = pool.getconn()
	cursor = conn.cursor()
	
	# Start by trying to convert identifier to integer to check if it's a unique_id
	try:
		identifier = int(identifier)
		lookup_column = "unique_id"
	except ValueError:
		# If it's not an int, we'll revert to treating it as a string and look up by 'book'
		lookup_column = "book"

	# Construct the SQL statement dynamically
	sql = f"UPDATE syllabus SET {column} = %s WHERE {lookup_column} = %s RETURNING *;"

	try:
		cursor.execute(sql, (new_value, identifier))
		updated_row = cursor.fetchone()
		conn.commit()

		if updated_row:
			message = f"Successfully updated {identifier} in column {column}."
		else:
			message = f"No matching item found for update."
	except psycopg2.Error as e:
		# Specific handling for commonly expected errors could be added here
		if "invalid input syntax" in str(e):
			print(f"Error: {e}")
			message = "The updated value provided is of the incorrect type for that column."
		else:
			message = f"Update to {identifier} in column {column} failed due to a database error."
	finally:
		# Ensure the cursor is always closed after the operation
		cursor.close()

	# Send the message to the Discord channel
	await send_and_delete(ctx, message)

@bot.command()
async def list_series(ctx, series_name):
	conn = pool.getconn()
	cursor = conn.cursor()

	# SQL query to select books from the specified series, ordered by num_in_series
	cursor.execute("""
		SELECT book, author, num_in_series 
		FROM syllabus 
		WHERE series = %s 
		ORDER BY num_in_series ASC
	""", (series_name,))

	rows = cursor.fetchall()

	# Check if there are any books in the series
	if rows:
		# Assuming author is the same for all books in the series and thus taking it from the first row
		author = rows[0][1] if rows[0][1] else "Unknown"
		message = f"*'{series_name}' - '{author}'*\n"

		# Format each book into a bulleted list
		for row in rows:
			book = row[0]
			num_in_series = row[2]
			message += f"- {book} (#{num_in_series})\n"
	else:
		message = "No books found in the specified series."

	await send_and_delete(ctx, message)

	cursor.close()
	pool.putconn(conn)

@bot.command()
async def columns(ctx):
	conn = pool.getconn()  # Get a connection from the pool
	cursor = conn.cursor()  # Open a cursor to perform database operations

	# Query to get the column names of the syllabus table
	query = """
	SELECT column_name 
	FROM information_schema.columns 
	WHERE table_name = 'syllabus' 
	ORDER BY ordinal_position;
	"""

	try:
		cursor.execute(query)
		columns = cursor.fetchall()  # Fetch all results
		column_names = [col[0] for col in columns]  # Extract column names from tuples

		# Format the column names into a string
		message = "Column names in the syllabus table:\n- " + "\n- ".join(column_names)
	except Exception as e:
		message = f"Failed to retrieve column names: {e}"

	await send_and_delete(ctx, message)  # Send the formatted message

	cursor.close()  # Don't forget to close the cursor
	pool.putconn(conn)  # Return the connection to the pool

# The command to display available commands
@bot.command()
async def cmds(ctx):
	conn = pool.getconn()
	cursor = conn.cursor()
	
	await send_and_delete(ctx, command_descriptions)

@bot.command()
async def report_bug(ctx, *, description: str):
	conn = pool.getconn()  # Get a database connection from the pool
	cursor = conn.cursor()  # Open a cursor to perform database operations

	# Check for the existence of the 'bugs' table
	cursor.execute("SELECT to_regclass('public.bugs');")
	if cursor.fetchone()[0] is None:
		# If the table doesn't exist, create it
		cursor.execute("""
			CREATE TABLE bugs (
				bug_id SERIAL PRIMARY KEY,
				description TEXT NOT NULL,
				added_by VARCHAR(255) NOT NULL
			);
		""")
	# Send a confirmation message
	await send_and_delete(ctx, "Bug report submitted successfully!")
	
	# Insert the new bug report into the 'bugs' table
	cursor.execute("""
		INSERT INTO bugs (description, added_by) VALUES (%s, %s);
	""", (description, ctx.author.name))
	conn.commit()  # Commit the transaction

	cursor.close()  # Close the cursor
	pool.putconn(conn)  # Return the connection to the pool

@bot.event
async def on_message(message):
	conn = pool.getconn()
	cursor = conn.cursor()
	
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
	# Run the bot
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
# organize the different commands in to different files or something so there's less scrolling
# follow tutorial https://www.youtube.com/watch?v=nW8c7vT6Hl4&list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ&ab_channel=Lucas to make modifications
# add support for the !help command which apparently will give a description automatically...
# see what happens if all of the @bots are changed to @client
# add a feature to determine who gets to choose the next book, who chose the last, and who has chosen how many, also a randomizer for who is next in the case of a tie
# add a feature to add a table for each book and then keep a list of or character fan-cast ideas for each book
# add a command to add a book to a season
# add a command to print all of the books in a season
# add a command to print all of the seasons and their books in the order the seasons occurred

# sources:
# https://docs.replit.com/tutorials/python/discord-role-bot
# https://docs.replit.com/tutorials/python/build-basic-discord-bot-python
# https://docs.replit.com/hosting/deployments/about-deployments
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.commands
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#commands
# Location for bot in discord: https://discord.com/developers/applications
# hosted: hosted on replit.com
