# Neon PostgreSQL Database Guide
**Setup and maintenance for the Teacher bot database**

---

## What Is Neon?

Neon is a serverless PostgreSQL hosting service. Your bot's database lives there — completely separate from both Replit and Google Cloud. This means the database keeps running no matter where the bot itself is hosted.

**Your database connection details:**
- **Host:** `ep-little-base-a5qoksxf.us-east-2.aws.neon.tech`
- **Database name:** `neondb`
- **User:** `neondb_owner`
- **Full connection string:** stored in `DATABASE_URL` in your `.env` file

---

## Accessing the Neon Dashboard

1. Go to [console.neon.tech](https://console.neon.tech)
2. Sign in with the account you used when you created the database
3. You'll see your project — click into it to see branches, tables, and usage

---

## Free Tier Limits

Neon's free plan includes:

| Resource | Limit |
|----------|-------|
| Projects | 1 |
| Storage | 10 GB |
| Compute hours | 191.9 hrs/month (enough for always-on at low usage) |
| Branches | 10 |

Your database is tiny compared to these limits, so you are unlikely to hit them.

> **Autosuspend:** On the free tier, Neon automatically pauses your database after 5 minutes
> of inactivity to save compute hours. The first query after a pause takes ~1 second longer
> while the database wakes up. This is normal and expected.

---

## Viewing Your Tables

### Option A — Neon SQL Editor (in browser)
1. Open your project in [console.neon.tech](https://console.neon.tech)
2. Click **"SQL Editor"** in the left sidebar
3. Type any SQL query and click **Run**

Useful queries to check your data:
```sql
-- See all tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Count rows in each main table
SELECT 'syllabus' AS tbl, COUNT(*) FROM syllabus
UNION ALL SELECT 'bugs', COUNT(*) FROM bugs
UNION ALL SELECT 'assignments', COUNT(*) FROM assignments
UNION ALL SELECT 'app_config', COUNT(*) FROM app_config;
```

### Option B — psql from your Google Cloud server
```bash
psql $DATABASE_URL
```
*(Requires `psql` to be installed: `sudo apt install postgresql-client -y`)*

---

## Backing Up Your Database

Run this from your Google Cloud server to export everything to a file:

```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

This creates a file like `backup_20260410.sql` containing all your data. Copy it somewhere safe (your local machine, Google Drive, etc.).

To restore from a backup:
```bash
psql $DATABASE_URL < backup_20260410.sql
```

> **Tip:** You can automate backups with a cron job on your Google Cloud server.
> Run `crontab -e` and add a line like:
> ```
> 0 3 * * * pg_dump $DATABASE_URL > ~/backups/backup_$(date +\%Y\%m\%d).sql
> ```
> This runs a backup every day at 3am.

---

## Checking Storage Usage

In the Neon dashboard, click your project and look at the **"Storage"** section in the overview. You can also query it directly:

```sql
SELECT pg_size_pretty(pg_database_size('neondb')) AS database_size;
```

---

## Resetting the Demo Tables

If the demo data gets cluttered, you can clear it without touching real data:

```sql
DELETE FROM demo_syllabus;
DELETE FROM demo_bugs;
DELETE FROM demo_assignments;
```

---

## Updating Your Connection String

If you ever need to rotate your database password or get a new connection string:

1. Go to [console.neon.tech](https://console.neon.tech)
2. Open your project → **"Connection Details"**
3. Copy the new connection string
4. Update `DATABASE_URL` in `~/bot/.env` on Google Cloud
5. Restart the bot: `pm2 restart teacher-bot --update-env`

---

## Migrating Away from Neon (Optional)

If you ever want to move the database to your Google Cloud VM instead:

### Step 1 — Install PostgreSQL on Google Cloud
```bash
sudo apt install postgresql postgresql-contrib postgresql-client -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 2 — Create a database and user
```bash
sudo -u postgres psql
```
Then inside the psql prompt:
```sql
CREATE USER teacher WITH PASSWORD 'choose_a_password';
CREATE DATABASE teacherdb OWNER teacher;
\q
```

### Step 3 — Export from Neon and import locally
```bash
pg_dump $DATABASE_URL > neon_export.sql
psql postgresql://teacher:choose_a_password@localhost/teacherdb < neon_export.sql
```

### Step 4 — Update your .env
```bash
nano ~/bot/.env
```
Change `DATABASE_URL` to:
```
DATABASE_URL=postgresql://teacher:choose_a_password@localhost/teacherdb
```
Then restart:
```bash
pm2 restart teacher-bot --update-env
```

---

## Troubleshooting

**Bot can't connect to the database?**
- Check that `DATABASE_URL` is set correctly in `~/bot/.env`
- Try connecting manually: `psql $DATABASE_URL`
- Neon's free tier may have suspended the database — the first connection after a pause can take ~1 second. Subsequent queries are normal speed.

**`psql` command not found?**
```bash
sudo apt install postgresql-client -y
```

**Table doesn't exist error?**
The app creates tables automatically on startup via SQLAlchemy. If a table is missing, restart the bot and it will be recreated:
```bash
pm2 restart teacher-bot
```
