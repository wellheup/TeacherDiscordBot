from discord.ext import commands
from sqlalchemy.orm import Session
from database import SessionLocal, Base
from crud import update_current_assignment, check_table_existing
from utils import send_and_delete

@commands.command()
async def update_assignment(ctx, description: str):
	db: Session = SessionLocal()
	is_demo = 'demo' in ctx.channel.name
	table_name = 'demo_assignments' if is_demo else 'assignments'
	try: 
		if check_table_existing(db, table_name) == False:
			message = f"The {table_name} table does not exist."
		else:
			assignment = update_current_assignment(db, description, is_demo)
			message = f"The current assignment is now: {assignment.description}, assigned on {assignment.date_added}"
	except Exception as e:
		message = f"An error occurred in updating assignment: {e}"
		print(message)
	finally:
		db.close()
	await send_and_delete(ctx, message)