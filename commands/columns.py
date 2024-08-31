from discord.ext import commands
from sqlalchemy.orm import Session

from crud import get_columns
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def columns(ctx):
    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    try:
        columns = get_columns(db, is_demo)
        message = "Column names in the syllabus table:\n- "
        message += "\n- ".join(columns)
    except Exception as e:
        message = f"Failed to retrieve column names: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)
