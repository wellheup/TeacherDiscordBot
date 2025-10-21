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
):
	db: Session = SessionLocal()
	is_demo = "demo" in ctx.channel.name
	try:
		assignment = add_assignment(db, description, is_demo)

		message = f"The new assignment is: {assignment.description}"
	except Exception as e:
		message = f"An error occurred in adding assignment: {e}"
		print(message)
	finally:
		db.close()
	return await send_and_delete(ctx, message)
