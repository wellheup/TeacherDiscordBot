from discord.ext import commands
from sqlalchemy.orm import Session
from database import SessionLocal, Base
from crud import add_bug, check_table_existing, create_bugs_table
from utils import send_and_delete

@commands.command()
async def report_bug(ctx, description: str):
    db: Session = SessionLocal()
    is_demo = 'demo' in ctx.channel.name
    table_name = 'demo_bugs' if is_demo else 'bugs'
    try:
        if check_table_existing(db, table_name) == False:
            create_bugs_table(db, table_name)
        add_bug(db, description, ctx.author.name, is_demo)
        
        message = f"Bug report submitted successfully! Thank you for your feedback."
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)