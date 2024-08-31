from discord.ext import commands
from sqlalchemy.orm import Session

from crud import get_series
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def list_series(ctx, series_name):
    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    try:
        rows = get_series(db, series_name, is_demo)
        if rows:
            # Assuming the author is the same for all books in
            # the series and thus taking it from the first row
            author = rows[0][1] if rows[0][1] else "Unknown"
            message = f"{series_name} by **{author}**\n"

            # Format each book into a bulleted list
            for row in rows:
                book = row[0]
                num_in_series = row[3]
                message += f"{num_in_series}.  *{book}*\n"
        else:
            message = "No books found in the specified series."
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)
