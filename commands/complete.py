from discord.ext import commands
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import complete
from utils import send_and_delete

@commands.command()
async def complete(ctx, item):
	db: Session = SessionLocal()
	is_demo = 'demo' in ctx.channel.name
	try: 
		book = complete(db, item, is_demo)
		message = f"Marked {book.book} as completed"
	except Exception as e:
		message = f"An error occurred: {e}"
		print(message)
	finally:
		db.close()
	await send_and_delete(ctx, message)