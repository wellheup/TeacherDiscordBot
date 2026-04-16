from datetime import datetime, timedelta

from discord.ext import commands
from sqlalchemy.orm import Session

from crud import add_assignment, check_table_existing
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def assign(
	ctx,
	description: str = commands.parameter(
		default=None, description="The assignment description"
	),
	due_date_str: str = commands.parameter(
		default=None, description="Due date in yyyy-mm-dd format (optional)"
	),
):
	db: Session = SessionLocal()
	is_demo = "demo" in ctx.channel.name
	try:
		due_date = None
		if due_date_str is not None:
			try:
				due_date = datetime.strptime(due_date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
			except ValueError:
				description = f"{description} {due_date_str}"
				due_date = None

		assignment = add_assignment(db, description, is_demo, due_date=due_date)
		message = (
			f"The new assignment is: {assignment.description}, "
			f"due: {assignment.due_date}"
		)
	except Exception as e:
		message = f"An error occurred in adding assignment: {e}"
		print(message)
	finally:
		db.close()
	return await send_and_delete(ctx, message)
