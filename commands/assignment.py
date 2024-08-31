from discord.ext import commands
from sqlalchemy.orm import Session

from crud import check_table_existing, get_current_assignment
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def assignment(ctx):
    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    table_name = "demo_assignments" if is_demo else "assignments"
    try:
        if check_table_existing(db, table_name) is False:
            message = f"The {table_name} table does not exist."
        else:
            assignment = get_current_assignment(db, is_demo)
            message = (
                f"The current assignment is: {assignment.description}, "
                f"assigned on {assignment.date_added}"
            )
    except Exception as e:
        message = f"An error occurred in retrieving assignment: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)
