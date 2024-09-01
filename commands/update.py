from discord.ext import commands
from sqlalchemy.orm import Session

from crud import update_book, update_id
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def update(
    ctx,
    book_id: int = commands.parameter(
        default=None, description="The id or title of the book to update"
    ),
    column: str = commands.parameter(default=None, description="The column to update"),
    new_value: str = commands.parameter(
        default=None, description="The new value for the column"
    ),
):
    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    try:
        if book_id.isdigit() and int(book_id) > 0:
            book = update_id(db, book_id, column, new_value, is_demo)
        else:
            book = update_book(db, book_id, column, new_value, is_demo)
        message = f"Updated {book.book} in column {column} " f"with value {new_value}"
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)
