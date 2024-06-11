from discord.ext import commands
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import remove_book, remove_id
from utils import send_and_delete

# The commmand to remove an item from the syllabus by name or unique_id
@commands.command()
async def remove(ctx, item):
    db: Session = SessionLocal()
    is_demo = 'demo' in ctx.channel.name
    try: 
        if item.isdigit() and int(item) > 0:
            book = remove_id(db, item, is_demo)
        else:
            book = remove_book(db, item, is_demo)
        message = f"Removed {book.book} from the syllabus"
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)