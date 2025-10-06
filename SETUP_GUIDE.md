# 📘 Complete Setup Guide

This guide will walk you through setting up the Politician Trade Tracker from scratch.

## Prerequisites

- **Docker** and **Docker Compose** installed ([Get Docker](https://docs.docker.com/get-docker/))
- An email account with SMTP access (Gmail, Outlook, etc.)
- 15 minutes of setup time

## Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/politician-trade-tracker.git
cd politician-trade-tracker
```

### Step 2: Configure Email Settings

#### A. Create your environment file

```bash
cp .env.example .env
```

#### B. Edit `.env` with your email credentials

Open `.env` in your favorite text editor:

```bash
nano .env
# or
code .env
```

#### C. Configure for Gmail (Recommended)

**Gmail requires an "App Password" - here's how to get one:**

1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Enable **2-Step Verification** (if not already enabled)
4. Go back to Security and click **App passwords** (or visit https://myaccount.google.com/apppasswords)
5. Select **Mail** and your device
6. Click **Generate**
7. Copy the 16-character password (no spaces)

**Update your `.env` file:**

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # Your 16-char app password
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=your-email@gmail.com  # Where you want to receive alerts
```

#### D. Configure for Other Email Providers

**Outlook/Hotmail:**
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
```

**Yahoo Mail:**
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your-email@yahoo.com
SMTP_PASSWORD=your-app-password  # Yahoo also requires app password
```

**Custom SMTP Server:**
```env
SMTP_HOST=smtp.yourdomain.com
SMTP_PORT=587  # or 465 for SSL
SMTP_USERNAME=your-username
SMTP_PASSWORD=your-password
```

### Step 3: Choose Politicians to Track

Edit `config.yaml`:

```bash
nano config.yaml
# or
code config.yaml
```

**Add or remove politicians from the list:**

```yaml
politicians:
  - Nancy Pelosi
  - Paul Pelosi      # Nancy's spouse
  - Tommy Tuberville
  - Dan Crenshaw
  - Josh Gottheimer
  - Ro Khanna
  # Add any member of Congress here!
```

**Adjust check frequency (optional):**

```yaml
check_interval_minutes: 60  # Default: check every hour
# Set to 30 for every 30 minutes
# Set to 1440 for once per day
```

### Step 4: Run with Docker

#### Start the application:

```bash
docker-compose up -d
```

This will:
- Build the Docker image
- Start the container in the background
- Begin checking for trades immediately

#### View the logs:

```bash
docker-compose logs -f
```

You should see output like:
```
Initializing Politician Trade Tracker...
Tracking 5 politician(s)
Check interval: 60 minutes
Testing email connection...
✓ Email connection successful
Checking for new trades...
```

Press `Ctrl+C` to exit the logs (container keeps running).

#### Stop the application:

```bash
docker-compose down
```

### Step 5: Verify Setup

#### Test email notifications:

```bash
# Run a one-time check
docker-compose run --rm politician-tracker python app/main.py --once
```

#### Check the database:

```bash
# View stored trades
docker exec -it politician-trade-tracker sqlite3 /app/data/trades.db "SELECT politician_name, ticker, transaction_type FROM trades LIMIT 5;"
```

## Alternative: Run Without Docker

If you prefer not to use Docker:

### 1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure `.env` (same as above)

### 3. Run the application:

```bash
# Run continuously
python app/main.py

# Or run once for testing
python app/main.py --once
```

## Troubleshooting

### "Email connection test failed"

**Problem:** Can't connect to SMTP server

**Solutions:**
- Double-check SMTP credentials in `.env`
- For Gmail: Make sure you're using an App Password, not your regular password
- Check that 2FA is enabled on your Google account
- Verify SMTP_HOST and SMTP_PORT are correct
- Some networks block port 587 - try port 465 with SSL

### "No trades detected"

**Problem:** The app isn't finding any trades

**Reasons:**
- Politicians may not have filed recent disclosures (normal)
- Trades can take days/weeks to be disclosed after the transaction
- Check if politician name spelling matches (use partial names like "Pelosi")
- The data source updates periodically

**Test with known politicians:**
```yaml
politicians:
  - Nancy Pelosi  # Very active trader
  - Paul Pelosi   # Nancy's spouse, also active
```

### Docker container won't start

**Check logs:**
```bash
docker-compose logs
```

**Rebuild the container:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Can't access database

**Enter the container:**
```bash
docker exec -it politician-trade-tracker sh
```

**View database:**
```bash
sqlite3 /app/data/trades.db
.tables
SELECT * FROM trades LIMIT 10;
.exit
```

## Advanced Configuration

### Change timezone:

Edit `docker-compose.yml`:
```yaml
environment:
  - TZ=America/Los_Angeles  # Change to your timezone
```

### Persist data across rebuilds:

The `data/` directory is already mounted as a volume, so your database persists even if you rebuild the container.

### Multiple email recipients:

Currently supports one email address. To send to multiple:
1. Use a comma-separated list in `EMAIL_TO`
2. Or set up email forwarding rules in your email client

### Custom data sources:

Edit `config.yaml`:
```yaml
data_source:
  type: custom
  url: https://your-data-source.com/api/trades.json
```

## Maintenance

### Update the application:

```bash
git pull origin main
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### View database statistics:

```bash
docker exec -it politician-trade-tracker sqlite3 /app/data/trades.db "SELECT politician_name, COUNT(*) as trade_count FROM trades GROUP BY politician_name;"
```

### Backup your database:

```bash
cp data/trades.db data/trades.db.backup
```

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Review this guide's troubleshooting section
3. Open an issue on GitHub with your logs (redact sensitive info)

## Security Notes

- Never commit your `.env` file to Git (it's in `.gitignore`)
- Use app passwords instead of real passwords when possible
- Keep your SMTP credentials secure
- The database only stores public information from Congressional disclosures

## What to Expect

- **First run:** May take a few minutes to fetch all historical trades
- **Subsequent runs:** Only new trades trigger emails
- **Email frequency:** Depends on how active your tracked politicians are
- **Data freshness:** Congressional disclosures can be delayed by days or weeks

Enjoy tracking Congressional trades! 🏛️📈
