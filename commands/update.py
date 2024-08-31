from discord.ext import commands
from sqlalchemy.orm import Session

from crud import update_book, update_id
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def update(ctx, item, column, new_value):
    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    try:
        if item.isdigit() and int(item) > 0:
            book = update_id(db, item, column, new_value, is_demo)
        else:
            book = update_book(db, item, column, new_value, is_demo)
        message = f"Updated {book.book} in column {column} " f"with value {new_value}"
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)
