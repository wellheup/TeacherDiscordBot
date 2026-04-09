import os
# Daily shifting URL
import random
import string
from datetime import datetime

import discord


async def send_and_delete(ctx, message, minutes=5):
        if minutes is not None:
                minutes = int(minutes) * 60
        allowed_mentions = discord.AllowedMentions.none()
        sent_message = None
        
        # Handle both Context and Message objects
        channel = getattr(ctx, "channel", ctx)
        # For Message objects, treat the Message itself as the target for reactions/deletion
        msg = getattr(ctx, "message", None) or (ctx if isinstance(ctx, discord.Message) else None)
        channel_name = getattr(channel, "name", "")
        
        if len(message) > 2000:
                message_parts = []
                current_part = ""
                for line in message.split("\n"):
                        if line.startswith("**"):
                                if current_part:
                                        message_parts.append(current_part)
                                        current_part = ""
                        current_part += f"{line}\n"
                message_parts.append(current_part)

                if "office-hours" in channel_name:
                        if msg:
                                await msg.add_reaction("👍")
                        for part in message_parts:
                                sent_message = await channel.send(part, allowed_mentions=allowed_mentions)
                else:
                        if msg:
                                await msg.delete()
                        for part in message_parts:
                                sent_message = await channel.send(
                                        part, delete_after=minutes, allowed_mentions=allowed_mentions
                                )
        else:
                if "office-hours" in channel_name:
                        sent_message = await channel.send(message, allowed_mentions=allowed_mentions)
                        if msg:
                                await msg.add_reaction("👍")
                else:
                        if msg:
                                await msg.delete()
                        sent_message = await channel.send(
                                message, delete_after=minutes, allowed_mentions=allowed_mentions
                        )
        return sent_message


# Daily shifting URL
def generate_random_string(length=8):
        """Generate a random string of fixed length"""
        letters = string.ascii_lowercase + string.digits
        return "".join(random.choice(letters) for i in range(length))


def get_config(key, default=None):
        """Retrieve a config value from the database"""
        from database import SessionLocal
        from models import AppConfig
        db = SessionLocal()
        try:
                config = db.query(AppConfig).filter(AppConfig.key == key).first()
                return config.value if config else default
        finally:
                db.close()


def set_config(key, value):
        """Store a config value in the database"""
        from database import SessionLocal
        from models import AppConfig
        db = SessionLocal()
        try:
                config = db.query(AppConfig).filter(AppConfig.key == key).first()
                if config:
                        config.value = value
                else:
                        config = AppConfig(key=key, value=value)
                        db.add(config)
                db.commit()
        finally:
                db.close()


def daily_update_url():
        """Update the URL in the database daily"""
        today = datetime.now().strftime("%Y-%m-%d")
        if get_config("last_update") != today:
                new_random_string = generate_random_string()
                set_config("url_suffix", new_random_string)
                set_config("last_update", today)
        return f"{os.environ['TEACHER_URL']}?url_suffix={get_config('url_suffix', '')}"


def get_current_url(is_demo=True):
        """Retrieve the current URL with the random suffix"""
        if is_demo:
                return f"{os.environ['TEACHER_URL']}"
        else:
                return f"{os.environ['TEACHER_URL']}?url_suffix={get_config('url_suffix', '')}"
