from discord.ext import commands
from sqlalchemy.orm import Session

from crud import get_todo
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def todo(
    ctx,
    minutes: int = commands.parameter(
        default=5,
        description="The number of minutes to keep the message, 0 for infinite",
    ),
):
    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    try:
        rows = get_todo(db, is_demo)
        currentAuthor = ""
        currentSeries = ""
        message = "**The following assignments have not yet been completed: **\n"

        for row in rows:
            book = f"*{row[0]}*"
            author = row[1]
            series = row[2]
            if author != currentAuthor:
                message += f"**{author}**\n"
                currentAuthor = author
            if series == "":
                currentSeries = series
                message += f"- {book} ({row[4]})\n"
            elif series != currentSeries:
                currentSeries = series
                message += f"- {currentSeries}\n"
                message += f"  - {book} ({row[4]})\n"
            else:
                message += f"  - {book} ({row[4]})\n"
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    return await send_and_delete(ctx, message)
