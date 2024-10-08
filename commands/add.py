from discord.ext import commands
from sqlalchemy.orm import Session

from crud import add_book
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def add(
    ctx,
    book: str = commands.parameter(default=None, description="Name of the book"),
    author: str = commands.parameter(default=None, description="Name of the author"),
    series: str = commands.parameter(
        default=None, description="Name of the book series"
    ),
    season: int = commands.parameter(
        default=0, description="Season the book was read during"
    ),
):
    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    try:
        book = add_book(
            db,
            book,
            author,
            series,
            ctx.author.name,
            season,
            is_demo,
            genre=None,
            is_extra_credit=False,
        )
        message = f"Added {book.book} to the syllabus"
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    return await send_and_delete(ctx, message)
