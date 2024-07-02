from discord.ext import commands
from sqlalchemy.orm import Session
from database import SessionLocal, Base
from crud import add_assignment, check_table_existing, create_assignments_table
from utils import send_and_delete
from datetime import datetime

@commands.command()
async def assign(ctx, description: str):
    db: Session = SessionLocal()
    is_demo = 'demo' in ctx.channel.name
    table_name = 'demo_assignments' if is_demo else 'assignments'
    date = await datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        if not check_table_existing(db, table_name):
            try:
                create_assignments_table(db, table_name)
            except Exception as e:
                message = f"Error creating table: {e}"
                print(message)
                await send_and_delete(ctx, message)
                return
        assignment = add_assignment(db, description, date, is_demo)

        message = f"The new assignment is: {assignment.description}"
    except Exception as e:
        message = f"An error occurred in adding the assignment: {e}"
        print(message)
    finally:
        try:
            db.close()
        except Exception as e:
            print(f"Failed to close the session: {e}")
    await send_and_delete(ctx, message)