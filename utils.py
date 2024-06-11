import discord

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