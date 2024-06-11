from discord.ext import commands
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import get_todo
from utils import send_and_delete

@commands.command()
async def todo(ctx, minutes: int = 5):
    db: Session = SessionLocal()
    is_demo = 'demo' in ctx.channel.name
    try:
        rows = get_todo(db, is_demo)
        currentAuthor = ''
        currentSeries = ''
        message = '**The following assignments have not yet been completed: **\n'

        for row in rows:
            book = f'*{row[0]}*'
            author = row[1]
            series = row[2]
            num_in_series = row[3]
            if author != currentAuthor:
                message += f'**{author}**\n'
                currentAuthor = author
            if series == '':
                currentSeries = series
                message += f'- {book} ({row[4]})\n'
            elif series != currentSeries:
                currentSeries = series
                message += f'- {currentSeries}\n'
                message += f'  - {book} ({row[4]})\n'
            else:
                message += f'  - {book} ({row[4]})\n'
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    finally:
        db.close()
    await send_and_delete(ctx, message)