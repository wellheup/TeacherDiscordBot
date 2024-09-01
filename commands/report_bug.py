from discord.ext import commands
from sqlalchemy.orm import Session

from crud import add_bug
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def report_bug(
    ctx,
    description: str = commands.parameter(
        default=None, description="The bug description"
    ),
):
    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    try:
        add_bug(db, description, ctx.author.name, is_demo)

        message_part1 = "Bug report submitted successfully!"
        message_part2 = " Thank you for your feedback."
        message = message_part1 + message_part2
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)
