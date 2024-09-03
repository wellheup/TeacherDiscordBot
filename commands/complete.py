from discord.ext import commands
from sqlalchemy.orm import Session

from crud import complete_book
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def complete(
    ctx,
    book: str = commands.parameter(default=None, description="The book to complete"),
):
    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    try:
        book = complete_book(db, book, is_demo)
        message = f"Marked {book.book} as completed"
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    return await send_and_delete(ctx, message)
