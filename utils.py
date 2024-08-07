import discord
import os

async def send_and_delete(ctx, message, minutes=5):
	if minutes != None:
		minutes = int(minutes) * 60
	allowed_mentions = discord.AllowedMentions.none()
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

		if 'office-hours' in ctx.channel.name:
			await ctx.message.add_reaction('👍')
			for part in message_parts:
				await ctx.send(part, allowed_mentions=allowed_mentions)
		else:
			await ctx.message.delete()
			for part in message_parts:
				await ctx.send(part, delete_after=minutes, allowed_mentions=allowed_mentions)
	else:
		if 'office-hours' in ctx.channel.name:
			await ctx.send(message, allowed_mentions=allowed_mentions)
			await ctx.message.add_reaction('👍')
		else:
			await ctx.message.delete()
			await ctx.send(message, delete_after=minutes, allowed_mentions=allowed_mentions)

# Daily shifting URL 
import random
import string
from replit import db
from datetime import datetime

def generate_random_string(length=8):
	"""Generate a random string of fixed length"""
	letters = string.ascii_lowercase + string.digits
	return ''.join(random.choice(letters) for i in range(length))
	
def daily_update_url():
	"""Update the URL in the database daily"""
	today = datetime.now().strftime("%Y-%m-%d")
	if db.get('last_update') != today:
		new_random_string = generate_random_string()
		db['url_suffix'] = new_random_string
		db['last_update'] = today
	return f"{os.environ['TEACHER_URL']}{db.get('url_suffix', '')}"
		
def get_current_url(is_demo=True):
	"""Retrieve the current URL with the random suffix"""
	if is_demo:
		f"{os.environ['TEACHER_URL']}"
	else:
		return f"{os.environ['TEACHER_URL']}{db.get('url_suffix', '')}"