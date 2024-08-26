from discord.ext import commands
from sqlalchemy.orm import Session

from crud import update_book, update_id
from database import SessionLocal
from utils import send_and_delete


@commands.command()
async def update(ctx, item, column, new_value):
    db: Session = SessionLocal()
    is_demo = "demo" in ctx.channel.name
    try:
        if item.isdigit() and int(item) > 0:
            book = update_id(db, item, column, new_value, is_demo)
        else:
            book = update_book(db, item, column, new_value, is_demo)
        message = f"Updated {book.book} in column {column} with value {new_value}"
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)


# from discord.ext import commands
# import psycopg2.pool
# from main import pool
# from utils import send_and_delete

# @commands.command()
# async def update(ctx, item, column, new_value):
#     conn = pool.getconn()
#     cursor = conn.cursor()
#     table = 'demo_syllabus' if 'demo' in ctx.channel.name else 'syllabus'

#     # Start by trying to convert item to integer to check if it's a unique_id
#     try:
#         item = int(item)
#         lookup_column = "unique_id"
#     except ValueError:
#         # If it's not an int, we'll revert to treating it as a string and look up by 'book'
#         lookup_column = "book"

#     # Construct the SQL statement dynamically
#     sql = f"UPDATE {table} SET {column} = %s WHERE {lookup_column} = %s RETURNING *;"

#     try:
#         cursor.execute(sql, (new_value, item))
#         updated_row = cursor.fetchone()
#         conn.commit()

#         if updated_row:
#             message = f"Successfully updated {item} in column {column}."
#         else:
#             message = f"No matching item found for update."
#     except psycopg2.Error as e:
#         # Specific handling for commonly expected errors could be added here
#         if "invalid input syntax" in str(e):
#             print(f"Error: {e}")
#             message = "The updated value provided is of the incorrect type for that column."
#         else:
#             message = f"Update to {item} in column {column} failed due to a database error."
#     finally:
#         # Ensure the cursor is always closed after the operation
#         cursor.close()

#     # Send the message to the Discord channel
#     await send_and_delete(ctx, message)
