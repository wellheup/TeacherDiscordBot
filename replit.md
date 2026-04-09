# Teacher Discord Bot & Web App

## Overview
This project combines a Discord bot ("Teacher") with a Flask web application. The bot manages assignments, syllabi, and student tasks while the web interface provides a visual dashboard.

## User Preferences

### Code Style
- **Indentation**: Use tabs instead of spaces for all Python files

## Recent Changes (October 21, 2025)

### Code Style Update
Converted all Python files to use tabs for indentation per user preference.

### Critical Bug Fixes - App Stability
Fixed several critical bugs that were causing the app to crash or become unresponsive:

1. **Fixed async function handling** - The `send_and_delete()` function was being called without `await`, causing silent failures and unresponsive behavior
2. **Removed duplicate Flask servers** - Eliminated the unused `keep_alive.py` file that was attempting to run a second Flask instance
3. **Fixed unreachable code** - Removed `keep_alive()` call that was placed after a blocking `bot.run()` call
4. **Enhanced robustness** - Updated `send_and_delete()` to properly handle both Discord Context objects (from commands) and Message objects (from event handlers)
5. **Fixed DM compatibility** - Added channel name guards to prevent crashes in DMs and threads
6. **Fixed missing return statement** - Corrected `get_current_url()` function in utils.py

## Project Architecture

### Main Components
- **main.py** - Entry point that runs Flask and Discord bot in separate threads
- **my_flask_app.py** - Flask web application
- **utils.py** - Shared utilities including `send_and_delete()` for Discord messaging
- **commands/** - Discord bot command modules
- **templates/** - HTML templates for Flask
- **static/** - CSS and JavaScript files

### Technology Stack
- Flask (web framework)
- discord.py (Discord bot)
- PostgreSQL (Neon hosted: `ep-little-base-a5qoksxf.us-east-2.aws.neon.tech`)
- SQLAlchemy ORM
- Threading (concurrent Flask + Discord bot execution)

### Database Tables
- `syllabus` / `demo_syllabus` — book reading list
- `bugs` / `demo_bugs` — bug reports
- `assignments` / `demo_assignments` — current assignments
- `app_config` — key-value config store (replaces Replit KV); stores `url_suffix` and `last_update`

## Deployment
- Target: Google Cloud Free Tier e2-micro (us-west1/us-central1/us-east1)
- Process manager: PM2 with Python venv
- See `cloud_setup.md` for full setup guide
- Dependencies for deployment: `requirements_deploy.txt`

## Current State
The application is running stably with both the Flask web server and Discord bot active. All critical bugs have been resolved. The `url_suffix` daily-rotating secret (used to gate write access on the web dashboard) is now stored in PostgreSQL (`app_config` table) instead of Replit's key-value store — removing the `replit` package dependency entirely.
