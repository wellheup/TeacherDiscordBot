from discord.ext import commands
from utils import get_current_url

@commands.command(name='url', aliases=['web'])
async def url(ctx):
    is_demo = 'demo' in ctx.channel.name
    current_url = get_current_url(is_demo)
    await ctx.send(f"The current URL is: {current_url}")