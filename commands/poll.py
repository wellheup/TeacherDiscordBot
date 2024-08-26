import asyncio

import discord
from discord.ext import commands
from sqlalchemy.orm import Session

from crud import find_book, find_id, update_book_poll
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def poll(ctx, item):
    from main import bot

    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    try:
        await ctx.message.add_reaction("👍")
        if item.isdigit() and int(item) > 0:
            row = find_id(db, item, is_demo)
        else:
            row = find_book(db, item, is_demo)

        if row:
            print(row)
            book_title = row[0]
            poll_message = await ctx.send(
                f"Would you like to read '{book_title}'?\n '💯' to end poll."
            )
            await poll_message.add_reaction("👍")
            await poll_message.add_reaction("👎")
            await poll_message.add_reaction("💯")

            def check(reaction, user):
                return str(reaction.emoji) == "💯" and user != bot.user

            await postResults(db, book_title, poll_message, row, is_demo)

            try:
                await bot.wait_for("reaction_add", timeout=20, check=check)
                await postResults()
            except asyncio.TimeoutError:
                await postResults()
        else:
            message = "No matching item found."
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)


async def postResults(db, book_title, poll_message, row, is_demo):
    from main import bot

    reaction_dict = discord.utils.get(bot.cached_messages, id=poll_message.id).reactions
    up_votes = 0
    down_votes = 0
    for reaction in reaction_dict:
        if str(reaction.emoji) == "👍":
            up_votes = reaction.count - 1  # Subtract 1 to exclude bot's reaction
        elif str(reaction.emoji) == "👎":
            down_votes = reaction.count - 1  # Subtract 1 to exclude bot's reaction

    update_book_poll(db, book_title, up_votes, down_votes, is_demo)

    result_message = await ctx.send(f"Up Votes: {up_votes}, Down Votes: {down_votes}")
    await result_message.add_reaction("💯")
    await poll_message.delete()
    try:
        await bot.wait_for("reaction_add", timeout=20, check=check)
        await result_message.delete()
    except asyncio.TimeoutError:
        await result_message.delete()
