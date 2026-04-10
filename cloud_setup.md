# Google Cloud Free Tier Setup Guide
**Discord Bot (Python/discord.py) + Flask Web App**

## What You Get (Free Forever)

| Resource | Amount |
|----------|--------|
| vCPU | 1 shared (e2-micro) |
| RAM | 1 GB |
| Storage | 30 GB |
| Network egress | 1 GB/month |
| External IP | Static, included |
| Expiry | Never |

> **Required regions:** You must use one of these or it won't be free:
> `us-west1` (Oregon), `us-central1` (Iowa), or `us-east1` (South Carolina)

---

## Part 1: Create Your Google Cloud Account

1. Go to [cloud.google.com](https://cloud.google.com)
2. Click **"Get started for free"**
3. Sign in with your Google account
4. Enter a credit card *(identity verification only — you won't be charged within free tier limits)*
5. Complete signup and land on the Google Cloud Console

---

## Part 2: Create Your Virtual Machine

1. Click the hamburger menu **☰** in the top left
2. Go to **Compute Engine → VM Instances**
3. If prompted, click **"Enable"** to enable the Compute Engine API *(takes about a minute)*
4. Click **"Create Instance"**
5. Give it a name like: `discord-bot`

### Region and Zone
- **Region:** Choose one of the free-eligible regions:
  - `us-west1` (Oregon)
  - `us-central1` (Iowa)
  - `us-east1` (South Carolina)
- **Zone:** Leave as the default for whichever region you pick

### Machine Configuration
- **Series:** E2
- **Machine type:** `e2-micro` *(the cost estimate on the right should show $0.00/month)*

### Boot Disk
- Click **"Change"**
- Operating System: **Ubuntu**
- Version: **Ubuntu 22.04 LTS**
- Boot disk type: **Standard persistent disk**
- Size: **30 GB** *(the free limit)*
- Click **"Select"**

### Networking
- **Virtual Cloud Network:** Leave as "Create new virtual cloud network"
- **Subnet:** Leave as "Create new public subnet"
- **Public IP Address:** Make sure **"Assign a public IPv4 address"** is set to **Yes**
  > This is critical — without it your bot and website won't be reachable from the internet

### Firewall
- Check **"Allow HTTP traffic"**
- Check **"Allow HTTPS traffic"**

6. Click **"Create"** and wait 1–2 minutes for the VM to start

---

## Part 3: Connect to Your Server

Google Cloud has a built-in browser SSH — no key files needed!

### Option A — Browser SSH Button (Easiest)
1. In the VM Instances list, find your `discord-bot` instance
2. Click the **"SSH"** button in the Connect column
3. A browser terminal opens — you're in! No key files, no extra setup.

### Option B — Termius (Polished)
A dedicated SSH client with a free tier and browser/desktop app.
Sign up at [termius.com](https://termius.com), then use your VM's external IP and the SSH key downloadable via the SSH dropdown menu.

### Option C — Terminal on Your Computer
1. Install Google Cloud CLI from [cloud.google.com/sdk](https://cloud.google.com/sdk)
2. Run:
```bash
gcloud compute ssh discord-bot --zone YOUR_ZONE
```

You should see a prompt like `your-username@discord-bot:~$` — you're in!

---

## Part 4: Install Python and Dependencies

Run these commands one at a time:

```bash
sudo apt update && sudo apt upgrade -y
```
*(This may take a few minutes)*

```bash
sudo apt install python3 python3-pip python3-venv git -y
```

After cloning your project in Part 5, you'll set up a virtual environment and install dependencies there. The commands are included in Part 5.

---

## Part 5: Clone Your Project from GitHub

Since your project is on GitHub, you can clone it directly to the server — no file uploads needed.

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git bot
cd bot
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

Then set up a virtual environment and install your dependencies:

```bash
cd ~/bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_deploy.txt
```

> **Why a virtual environment?** Newer Ubuntu versions block system-wide pip installs to
> protect the OS. A virtual environment is an isolated space just for your project's packages.
> You'll see `(venv)` at the start of your prompt when it's active.

> **Note:** Your `.env` file with secrets should NOT be in your GitHub repo.
> You'll create that manually in the next step.

---

## Part 6: Set Up Your Secrets / Environment Variables

Your secrets are not stored in GitHub (and shouldn't be). Create a `.env` file manually on the server:

```bash
cd ~/bot
nano .env
```

In the text editor that opens, add your secrets:

```
DISCORD_BOT_SECRET=your_discord_token_here
TEACHER_URL=http://YOUR_EXTERNAL_IP:5000
DATABASE_URL=your_postgresql_connection_string_here
```

Save by pressing **Ctrl+X**, then **Y**, then **Enter**

### Where to find these values
- **DISCORD_BOT_SECRET** — from the [Discord Developer Portal](https://discord.com/developers/applications), under your bot's "Bot" tab → "Token"
- **TEACHER_URL** — your Google Cloud VM's external IP address (visible in VM Instances list), formatted as `http://YOUR_EXTERNAL_IP:5000`
- **DATABASE_URL** — your Neon (or other) PostgreSQL connection string

> **TEACHER_URL is important:** This controls the URL the bot posts when users run `!web`.
> Set it to your Google Cloud server's external IP so it points to your Flask app,
> not the old Replit deployment.

---

## Updating Your .env Values Later

To change any secret or environment variable after initial setup:

```bash
nano ~/bot/.env
```

Use the arrow keys to navigate to the line you want to change, edit the value, then save with **Ctrl+X → Y → Enter**.

After saving, restart the bot to pick up the new values:

```bash
pm2 restart teacher-bot --update-env
```

> **Important:** You must include `--update-env` any time you change `.env` values.
> A plain `pm2 restart` reuses the cached environment from when the process first started
> and will **not** pick up your changes.

### Common things you might need to update

| Variable | When to update |
|----------|---------------|
| `DISCORD_BOT_SECRET` | If you regenerate your bot token in Discord |
| `TEACHER_URL` | If your server's external IP changes, or you set up a domain |
| `DATABASE_URL` | If you move your database to a different host |
| `BOT_PREFIX` | If you want commands to use a different prefix (default is `!`) |

> **BOT_PREFIX tip:** The bot defaults to `!` (e.g. `!web`, `!cmds`). If you run a second copy
> of the bot for development on Replit, set `BOT_PREFIX=.` in Replit's Secrets so the two bots
> don't respond to the same commands at the same time.

> **Tip:** To quickly check your server's current external IP without leaving the terminal:
> ```bash
> curl ifconfig.me
> ```

---

## Part 7: Open the Firewall for Your Web App

Google Cloud manages firewall rules through VPC Firewall Rules:

1. In Google Cloud Console, click **☰**
2. Go to **VPC Network → Firewall**
3. Click **"Create Firewall Rule"**
4. Set the following:
   - **Name:** `allow-flask`
   - **Direction:** Ingress
   - **Action on match:** Allow
   - **Targets:** All instances in the network
   - **Source IPv4 ranges:** `0.0.0.0/0`
   - **Protocols and ports:** TCP, port `5000`
5. Click **"Create"**

Also run this in your SSH window to allow it through Ubuntu's internal firewall:

```bash
sudo iptables -I INPUT -p tcp --dport 5000 -j ACCEPT
```

---

## Part 8: Keep Your Bot Running 24/7 with PM2

Install PM2 — it keeps your app running and auto-restarts it if it crashes:

```bash
sudo apt install nodejs npm -y
sudo npm install -g pm2
```

Start your bot, pointing PM2 to your virtual environment's Python:

```bash
cd ~/bot
pm2 start main.py --name teacher-bot --interpreter ~/bot/venv/bin/python3
```

Make it restart automatically if the server reboots:

```bash
pm2 save
pm2 startup
```
*(Copy and run the command that PM2 outputs)*

### Useful PM2 Commands

```bash
pm2 status                             # Check if your bot is running
pm2 logs teacher-bot                   # View live logs
pm2 restart teacher-bot                # Restart after code changes
pm2 restart teacher-bot --update-env   # Restart AND reload .env changes
pm2 stop teacher-bot                   # Stop the bot
```

---

## Part 9: Updating Your Bot in the Future

Whenever you push changes to GitHub, updating your server is straightforward:

```bash
cd ~/bot
git pull
pm2 restart teacher-bot
```

If you've added new packages to `requirements_deploy.txt`, also run:

```bash
source ~/bot/venv/bin/activate
pip install -r requirements_deploy.txt
pm2 restart teacher-bot
```

That's it — no file uploads or zipping needed.

---

## Notes About Your Database

Your Replit PostgreSQL database stays accessible via its `DATABASE_URL` even after moving your bot to Google Cloud. The recommended approach:

- **Keep the database on Replit** — no migration needed
- Copy your `DATABASE_URL` into the `.env` file on Google Cloud (Part 6)
- Your bot will connect to Replit's database from Google's server

If you ever want to fully move off Replit, you can install PostgreSQL directly on the VM:

```bash
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

Then update `DATABASE_URL` in your `.env` to point to `localhost`.

> **RAM note:** The e2-micro only has 1 GB RAM. Running both the Discord bot and Flask app
> together should be fine for light usage. If you notice slowdowns, consider hosting the
> Flask web app on [Render.com](https://render.com)'s free tier separately.

---

## Troubleshooting

**Bot not starting?**
```bash
pm2 logs teacher-bot
```
Check for error messages in the output.

**Can't reach the website?**
- Double-check Part 7 (firewall rules in Google Cloud Console)
- Make sure Flask is running: `pm2 status`
- Try `http://YOUR_EXTERNAL_IP:5000` in your browser

**Running out of memory?**
```bash
free -h
```
If consistently low, consider moving the Flask web app to Render.com (free) and only running the bot here.

**VM stopped unexpectedly?**
- Google Cloud may stop free tier VMs if it detects no usage
- PM2's startup command (Part 8) will restart your bot automatically when the VM comes back online
- Log into Google Cloud Console and restart the VM manually if needed

**Need to re-clone after something breaks?**
```bash
cd ~
rm -rf bot
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git bot
cd bot
pip3 install -r requirements_deploy.txt
```
Then recreate your `.env` file (Part 6) and restart PM2 (Part 8).
