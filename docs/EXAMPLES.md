# 📧 Example Email Notifications

This document shows what you can expect from the email notifications.

## Sample Email Output

### Subject Line
```
[Politician Trade Alert] 3 New Trade(s) Detected
```

### Email Body (HTML)

```
🏛️ Politician Trade Alert
Detected 3 new trade(s)

┌─────────────────────────────────────────┐
│ Nancy Pelosi                            │
├─────────────────────────────────────────┤
│ Ticker: NVDA                            │
│ Asset: NVIDIA Corporation Stock         │
│ Transaction: Purchase ✅                 │
│ Amount Range: $1,000,001 - $5,000,000   │
│ Transaction Date: 2024-09-15            │
│ Disclosure Date: 2024-09-30             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Paul Pelosi                             │
├─────────────────────────────────────────┤
│ Ticker: MSFT                            │
│ Asset: Microsoft Corporation Stock      │
│ Transaction: Sale ❌                     │
│ Amount Range: $250,001 - $500,000       │
│ Transaction Date: 2024-09-20            │
│ Disclosure Date: 2024-10-01             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Tommy Tuberville                        │
├─────────────────────────────────────────┤
│ Ticker: AAPL                            │
│ Asset: Apple Inc. Stock                 │
│ Transaction: Purchase ✅                 │
│ Amount Range: $50,001 - $100,000        │
│ Transaction Date: 2024-09-18            │
│ Disclosure Date: 2024-09-29             │
└─────────────────────────────────────────┘

Generated: 2024-10-06 14:30:15
```

## Color Coding

In HTML emails:
- **Purchase** transactions appear in 🟢 **GREEN**
- **Sale** transactions appear in 🔴 **RED**
- **Exchange** transactions appear in 🟡 **YELLOW**

## Email Frequency

### Normal Operation
- You'll receive emails **only when new trades are detected**
- If no new trades: **No email** (no spam!)
- Multiple trades are batched into a single email

### Example Timeline

**Day 1 (Monday 10 AM):**
- App checks for trades
- Finds 3 new Nancy Pelosi trades
- Sends 1 email with all 3 trades

**Day 1 (Monday 11 AM):**
- App checks again
- No new trades found
- No email sent ✅

**Day 2 (Tuesday 10 AM):**
- App checks for trades
- Finds 1 new Tommy Tuberville trade
- Sends 1 email with that trade

## Configuration Examples

### Example 1: Track Only Pelosi

**config.yaml:**
```yaml
politicians:
  - Nancy Pelosi
  - Paul Pelosi

check_interval_minutes: 60
```

**Result:**
- Checks every hour
- Only notifies about Pelosi trades
- Low email volume (Pelosi trades weekly/monthly)

### Example 2: Track Top Traders

**config.yaml:**
```yaml
politicians:
  - Nancy Pelosi
  - Paul Pelosi
  - Tommy Tuberville
  - Josh Gottheimer
  - Dan Crenshaw
  - Ro Khanna

check_interval_minutes: 30
```

**Result:**
- Checks every 30 minutes
- More comprehensive tracking
- Higher email volume (these are active traders)

### Example 3: Daily Digest

**config.yaml:**
```yaml
politicians:
  - Nancy Pelosi

check_interval_minutes: 1440  # Once per day
```

**Result:**
- Checks once per day
- Batches all daily trades into one email
- Low email frequency

## Command Line Examples

### Run Once (Testing)
```bash
# Test email configuration
python app/main.py --once
```

**Expected output:**
```
Initializing Politician Trade Tracker...
Tracking 2 politician(s)
Check interval: 60 minutes
Testing email connection...
✓ Email connection successful
============================================================
Checking for new trades...
Fetching trades from https://senate-stock-watcher-data...
Fetched 12847 total transactions
New trade: Nancy Pelosi - NVDA (Purchase)
New trade: Nancy Pelosi - MSFT (Sale)
Found 2 new trade(s)
Successfully sent email alert for 2 trade(s)
Notified 2 trade(s)
Check completed
============================================================
```

### Run Continuously
```bash
# Run in foreground
python app/main.py
```

**Expected output:**
```
Starting Politician Trade Tracker...
Will check every 60 minutes
Testing email connection...
✓ Email connection successful
============================================================
Checking for new trades...
Found 3 new trade(s)
Successfully sent email alert for 3 trade(s)
Check completed
============================================================
[Waits 60 minutes]
============================================================
Checking for new trades...
No new trades found
Check completed
============================================================
```

## Docker Examples

### View Live Logs
```bash
docker-compose up
# or for background:
docker-compose up -d
docker-compose logs -f
```

### Check Trade Database
```bash
# View all trades
docker exec -it politician-trade-tracker sqlite3 /app/data/trades.db \
  "SELECT politician_name, ticker, transaction_type, transaction_date FROM trades ORDER BY transaction_date DESC LIMIT 10;"
```

**Output:**
```
Nancy Pelosi|NVDA|Purchase|2024-09-15
Paul Pelosi|MSFT|Sale|2024-09-20
Tommy Tuberville|AAPL|Purchase|2024-09-18
```

### Count Trades by Politician
```bash
docker exec -it politician-trade-tracker sqlite3 /app/data/trades.db \
  "SELECT politician_name, COUNT(*) as trade_count FROM trades GROUP BY politician_name ORDER BY trade_count DESC;"
```

**Output:**
```
Nancy Pelosi|156
Paul Pelosi|98
Tommy Tuberville|87
Josh Gottheimer|45
```

## Troubleshooting Examples

### Test Email Without Running Full App
```python
# Create test_email.py
from app.config import Config
from app.email_service import EmailService
from app.models import Trade
from datetime import datetime

config = Config()
email = EmailService(config)

# Create test trade
test_trade = Trade(
    politician_name="Test Politician",
    ticker="TEST",
    transaction_type="Purchase",
    amount_range="$1,001 - $15,000",
    transaction_date=datetime.now(),
    disclosure_date=datetime.now(),
    asset_description="Test Stock"
)

# Send test email
email.send_trade_alert([test_trade])
```

### Check If SMTP Credentials Work
```bash
python -c "
from app.config import Config
from app.email_service import EmailService

config = Config()
email = EmailService(config)
print('Testing connection...')
success = email.test_connection()
print('✓ Success!' if success else '✗ Failed')
"
```

## Data Source Examples

The app fetches data from Senate Stock Watcher. Example API response:

```json
{
  "senator": "Nancy Pelosi",
  "ticker": "NVDA",
  "asset_description": "NVIDIA Corporation",
  "transaction_type": "Purchase",
  "transaction_date": "2024-09-15",
  "disclosure_date": "2024-09-30",
  "amount": "$1,000,001 - $5,000,000",
  "comment": ""
}
```

## Popular Politicians & Expected Volume

| Politician | Typical Trades/Year | Email Frequency |
|------------|---------------------|-----------------|
| Nancy Pelosi | 50-100 | ~1-2/week |
| Paul Pelosi | 100-200 | ~2-4/week |
| Tommy Tuberville | 200-300 | Daily during active periods |
| Josh Gottheimer | 30-60 | ~1/week |
| Dan Crenshaw | 20-40 | ~1-2/month |

## Real-World Usage

### Scenario 1: Passive Monitoring
> "I want to know when Nancy Pelosi makes big tech trades"

**Setup:**
```yaml
politicians:
  - Nancy Pelosi
check_interval_minutes: 240  # Check 4x per day
```

**Result:** Low maintenance, few emails, focused on one person

### Scenario 2: Active Tracking
> "I want to track the most active Congressional traders"

**Setup:**
```yaml
politicians:
  - Nancy Pelosi
  - Paul Pelosi
  - Tommy Tuberville
  - Josh Gottheimer
  - Brian Higgins
  - Shelley Capito
check_interval_minutes: 60
```

**Result:** Higher email volume, comprehensive coverage

### Scenario 3: Research Project
> "I'm researching Congressional trading patterns"

**Setup:**
```yaml
# Track everyone (add 50+ politicians)
check_interval_minutes: 60
```

**Result:** High email volume, full dataset for analysis

## Next Steps

- See [SETUP_GUIDE.md](../SETUP_GUIDE.md) for installation
- See [README.md](../README.md) for overview
- See [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute
