"""Main application for politician trade tracking and email notifications."""

import logging
import time
import requests
from datetime import datetime
from typing import List, Dict, Any
import schedule

from models import Database
from config import Config
from email_service import EmailService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PoliticianTradeTracker:
    """Main application for tracking politician trades."""

    def __init__(self, config_path='config.yaml'):
        """Initialize the trade tracker."""
        logger.info("Initializing Politician Trade Tracker...")

        # Load configuration
        self.config = Config(config_path)
        is_valid, errors = self.config.validate()
        if not is_valid:
            for error in errors:
                logger.error(f"Configuration error: {error}")
            raise ValueError("Invalid configuration")

        # Initialize services
        self.db = Database(self.config.database_path)
        self.email_service = EmailService(self.config)

        logger.info(f"Tracking {len(self.config.politicians)} politician(s)")
        logger.info(f"Check interval: {self.config.check_interval_minutes} minutes")

    def fetch_trades(self) -> List[Dict[str, Any]]:
        """Fetch latest trades from data source."""
        try:
            logger.info(f"Fetching trades from {self.config.data_source_url}")
            response = requests.get(self.config.data_source_url, timeout=30)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Fetched {len(data)} total transactions")
            return data

        except requests.RequestException as e:
            logger.error(f"Failed to fetch trades: {e}")
            return []

    def parse_trade_data(self, raw_trade: Dict[str, Any]) -> Dict[str, Any]:
        """Parse raw trade data into database format."""
        # Parse dates
        transaction_date = None
        disclosure_date = None

        try:
            if raw_trade.get('transaction_date'):
                transaction_date = datetime.strptime(raw_trade['transaction_date'], '%Y-%m-%d')
        except (ValueError, TypeError):
            pass

        try:
            if raw_trade.get('disclosure_date'):
                disclosure_date = datetime.strptime(raw_trade['disclosure_date'], '%Y-%m-%d')
        except (ValueError, TypeError):
            disclosure_date = datetime.utcnow()

        # Parse amount range
        amount_range = raw_trade.get('amount', '')
        amount_min, amount_max = self._parse_amount_range(amount_range)

        return {
            'politician_name': raw_trade.get('senator', raw_trade.get('representative', 'Unknown')),
            'transaction_date': transaction_date,
            'disclosure_date': disclosure_date,
            'ticker': raw_trade.get('ticker', 'N/A'),
            'asset_description': raw_trade.get('asset_description', ''),
            'asset_type': raw_trade.get('type', ''),
            'transaction_type': raw_trade.get('transaction_type', 'Unknown'),
            'amount_range': amount_range,
            'amount_min': amount_min,
            'amount_max': amount_max,
            'comment': raw_trade.get('comment', ''),
            'notified': False
        }

    def _parse_amount_range(self, amount_str: str) -> tuple[float, float]:
        """Parse amount range string into min and max values."""
        if not amount_str:
            return 0.0, 0.0

        # Example: "$1,001 - $15,000" or "$50,001 - $100,000"
        try:
            parts = amount_str.replace('$', '').replace(',', '').split(' - ')
            if len(parts) == 2:
                return float(parts[0]), float(parts[1])
        except (ValueError, AttributeError):
            pass

        return 0.0, 0.0

    def filter_tracked_politicians(self, trades: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter trades to only include tracked politicians."""
        tracked = []
        for trade in trades:
            politician_name = trade.get('politician_name', '').lower()
            for tracked_politician in self.config.politicians:
                if tracked_politician.lower() in politician_name:
                    tracked.append(trade)
                    break
        return tracked

    def process_new_trades(self) -> List:
        """Process new trades and return those that need notification."""
        # Fetch latest trades
        raw_trades = self.fetch_trades()
        if not raw_trades:
            logger.info("No trades fetched")
            return []

        # Parse and filter trades
        new_trades = []
        for raw_trade in raw_trades:
            try:
                parsed_trade = self.parse_trade_data(raw_trade)

                # Filter by tracked politicians
                if not any(pol.lower() in parsed_trade['politician_name'].lower()
                          for pol in self.config.politicians):
                    continue

                # Check if trade already exists
                if not self.db.trade_exists(
                    parsed_trade['politician_name'],
                    parsed_trade['ticker'],
                    parsed_trade['transaction_date'],
                    parsed_trade['transaction_type']
                ):
                    # Add to database
                    trade = self.db.add_trade(parsed_trade)
                    new_trades.append(trade)
                    logger.info(f"New trade: {trade.politician_name} - {trade.ticker} ({trade.transaction_type})")

            except Exception as e:
                logger.error(f"Error processing trade: {e}")
                continue

        return new_trades

    def send_notifications(self, trades: List) -> bool:
        """Send email notifications for new trades."""
        if not trades:
            return True

        if not self.config.email_enabled:
            logger.info("Email notifications disabled")
            return True

        # Send email
        success = self.email_service.send_trade_alert(trades)

        if success:
            # Mark trades as notified
            for trade in trades:
                self.db.mark_as_notified(trade.id)
            logger.info(f"Notified {len(trades)} trade(s)")
        else:
            logger.error("Failed to send notifications")

        return success

    def check_for_new_trades(self):
        """Main task: Check for new trades and send notifications."""
        logger.info("=" * 60)
        logger.info("Checking for new trades...")

        try:
            # Process new trades
            new_trades = self.process_new_trades()

            if new_trades:
                logger.info(f"Found {len(new_trades)} new trade(s)")
                self.send_notifications(new_trades)
            else:
                logger.info("No new trades found")

        except Exception as e:
            logger.error(f"Error checking for trades: {e}")

        logger.info("Check completed")
        logger.info("=" * 60)

    def run_once(self):
        """Run the tracker once (for testing)."""
        logger.info("Running one-time check...")
        self.check_for_new_trades()

    def run(self):
        """Run the tracker continuously on schedule."""
        logger.info("Starting Politician Trade Tracker...")
        logger.info(f"Will check every {self.config.check_interval_minutes} minutes")

        # Test email connection
        if self.config.email_enabled:
            logger.info("Testing email connection...")
            if self.email_service.test_connection():
                logger.info("✓ Email connection successful")
            else:
                logger.warning("✗ Email connection failed - check your configuration")

        # Schedule the task
        schedule.every(self.config.check_interval_minutes).minutes.do(self.check_for_new_trades)

        # Run immediately on start
        self.check_for_new_trades()

        # Run scheduled tasks
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute for scheduled tasks
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.db.close()


def main():
    """Main entry point."""
    import sys

    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        tracker = PoliticianTradeTracker()
        tracker.run_once()
    else:
        tracker = PoliticianTradeTracker()
        tracker.run()


if __name__ == '__main__':
    main()
