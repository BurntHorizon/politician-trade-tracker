# 🏛️ Politician Trade Tracker

A Docker-based application that monitors Congressional stock trades and sends email notifications when tracked politicians make new trades. Track any member of Congress and get instant alerts about their stock transactions.

## Features

- ✅ **Multi-Politician Tracking** - Monitor any members of Congress
- 📧 **Email Notifications** - Receive formatted emails with trade details
- 🐳 **Docker Support** - Easy deployment with Docker Compose
- 💾 **SQLite Database** - Tracks trades to avoid duplicate notifications
- ⚙️ **Configurable** - Easy YAML configuration for politicians and settings
- 🔄 **Scheduled Checks** - Automatic periodic checking for new trades
- 📊 **Rich Email Format** - HTML emails with color-coded buy/sell indicators

## Quick Start

### 1. Clone/Download

```bash
cd /Users/alex/Coding/Pelosi_tech
```

### 2. Configure Email Settings

Copy the example environment file and add your SMTP credentials:

```bash
cp .env.example .env
```

Edit `.env` with your email settings:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=recipient@example.com
```

**Gmail Setup:**
1. Enable 2-Factor Authentication
2. Generate an app password at https://myaccount.google.com/apppasswords
3. Use that password in `SMTP_PASSWORD`

### 3. Choose Politicians to Track

Edit `config.yaml` to select which politicians to monitor:

```yaml
politicians:
  - Nancy Pelosi
  - Paul Pelosi
  - Tommy Tuberville
  - Dan Crenshaw
  # Add any member of Congress here
```

You can also adjust the check interval:

```yaml
check_interval_minutes: 60  # Check every hour
```

### 4. Run with Docker (Recommended)

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### 5. Run without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app/main.py

# Or run once for testing
python app/main.py --once
```

## Configuration

### config.yaml

Main configuration file for the application:

- **politicians**: List of politicians to track (case-insensitive, partial match)
- **check_interval_minutes**: How often to check for new trades
- **email.enabled**: Enable/disable email notifications
- **email.subject_prefix**: Prefix for email subjects

### .env

Environment variables for sensitive data:

- **SMTP_HOST**: SMTP server hostname
- **SMTP_PORT**: SMTP server port (usually 587)
- **SMTP_USERNAME**: Your email username
- **SMTP_PASSWORD**: Your email password/app password
- **EMAIL_FROM**: Sender email address
- **EMAIL_TO**: Recipient email address
- **DATABASE_PATH**: Path to SQLite database

## Data Source

This application uses the [Senate Stock Watcher](https://senatestockwatcher.com/) public dataset, which aggregates Congressional financial disclosure data. The data includes:

- Transaction dates
- Disclosure dates
- Stock tickers
- Transaction types (Purchase/Sale/Exchange)
- Amount ranges
- Asset descriptions

## Email Notifications

When new trades are detected, you'll receive an HTML email with:

- Politician name
- Stock ticker symbol
- Transaction type (color-coded: green for purchases, red for sales)
- Amount range
- Transaction and disclosure dates
- Asset description

## Project Structure

```
Pelosi_tech/
├── app/
│   ├── main.py           # Main application logic
│   ├── models.py         # Database models
│   ├── config.py         # Configuration management
│   └── email_service.py  # Email notification service
├── data/                 # SQLite database (created automatically)
├── config.yaml           # Main configuration
├── .env                  # Environment variables (create from .env.example)
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image definition
└── docker-compose.yml    # Docker Compose configuration
```

## Popular Politicians to Track

Some of the most active Congressional traders:

- **Nancy Pelosi** (D-CA) - Former House Speaker
- **Paul Pelosi** - Nancy's spouse, very active trader
- **Tommy Tuberville** (R-AL) - Senator
- **Josh Gottheimer** (D-NJ) - Representative
- **Dan Crenshaw** (R-TX) - Representative
- **Ro Khanna** (D-CA) - Representative
- **Mark Green** (R-TN) - Representative
- **Pat Fallon** (R-TX) - Representative

Simply add their names to the `politicians` list in `config.yaml`.

## Troubleshooting

### Email not sending

1. Verify SMTP credentials in `.env`
2. For Gmail, ensure you're using an App Password, not your regular password
3. Check the logs: `docker-compose logs -f`
4. Test the connection: Run with `--once` flag to do a single check

### No trades detected

1. The data source updates periodically as politicians file disclosures
2. Trades may take days or weeks to appear after the transaction
3. Check if the politician name matches exactly (use partial names)
4. View recent trades in the database: `sqlite3 data/trades.db "SELECT * FROM trades LIMIT 10;"`

### Docker issues

```bash
# Rebuild the container
docker-compose build --no-cache

# Check if container is running
docker ps

# View detailed logs
docker-compose logs --tail=100 -f
```

## Development

To run in development mode:

```bash
# Install dependencies
pip install -r requirements.txt

# Run once for testing
python app/main.py --once

# Run continuously
python app/main.py
```

## License

This project is for educational and informational purposes only. Congressional financial disclosure data is public information.

## Disclaimer

This tool monitors publicly available Congressional financial disclosures. It does not provide investment advice. Always do your own research before making investment decisions.
