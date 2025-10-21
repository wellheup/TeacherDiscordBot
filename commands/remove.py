from discord.ext import commands
from sqlalchemy.orm import Session

from crud import remove_book, remove_id
from database import SessionLocal
from utils import send_and_delete


# The commmand to remove an item from the syllabus by name or unique_id
@commands.command()
async def remove(
	ctx,
	book: str = commands.parameter(
		default=None, description="Name or id of the book to remove"
	),
):
	db: Session = SessionLocal()
	is_demo = "demo" in ctx.channel.name
	try:
		if book.isdigit() and int(book) > 0:
			book = remove_id(db, book, is_demo)
		else:
			book = remove_book(db, book, is_demo)
		message = f"Removed {book.book} from the syllabus"
	except Exception as e:
		message = f"An error occurred: {e}"
		print(message)
	finally:
		db.close()
	return await send_and_delete(ctx, message)
