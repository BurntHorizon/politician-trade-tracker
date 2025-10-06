"""Email notification service for politician trade alerts."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending email notifications about politician trades."""

    def __init__(self, config):
        """Initialize email service with configuration."""
        self.config = config
        self.smtp_host = config.smtp_host
        self.smtp_port = config.smtp_port
        self.smtp_username = config.smtp_username
        self.smtp_password = config.smtp_password
        self.email_from = config.email_from
        self.email_to = config.email_to
        self.subject_prefix = config.email_subject_prefix

    def send_trade_alert(self, trades: List) -> bool:
        """Send email alert for new trades."""
        if not trades:
            logger.info("No trades to send")
            return True

        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"{self.subject_prefix} {len(trades)} New Trade(s) Detected"
            msg['From'] = self.email_from
            msg['To'] = self.email_to

            # Create email body
            html_body = self._create_html_body(trades)
            text_body = self._create_text_body(trades)

            # Attach both plain text and HTML versions
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Successfully sent email alert for {len(trades)} trade(s)")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def _create_text_body(self, trades: List) -> str:
        """Create plain text email body."""
        lines = [
            "New Politician Trade Alert",
            "=" * 50,
            "",
            f"Detected {len(trades)} new trade(s):",
            ""
        ]

        for trade in trades:
            lines.extend([
                f"Politician: {trade.politician_name}",
                f"Ticker: {trade.ticker}",
                f"Asset: {trade.asset_description or 'N/A'}",
                f"Transaction: {trade.transaction_type}",
                f"Amount Range: {trade.amount_range or 'N/A'}",
                f"Transaction Date: {trade.transaction_date.strftime('%Y-%m-%d') if trade.transaction_date else 'N/A'}",
                f"Disclosed: {trade.disclosure_date.strftime('%Y-%m-%d') if trade.disclosure_date else 'N/A'}",
                "-" * 50,
                ""
            ])

        lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(lines)

    def _create_html_body(self, trades: List) -> str:
        """Create HTML email body."""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                .container { max-width: 800px; margin: 0 auto; padding: 20px; }
                .header { background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
                .trade-card {
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 15px 0;
                    background-color: #f9f9f9;
                }
                .trade-header {
                    font-size: 18px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }
                .trade-detail {
                    margin: 5px 0;
                    font-size: 14px;
                }
                .label {
                    font-weight: bold;
                    color: #555;
                }
                .buy { color: #27ae60; }
                .sell { color: #e74c3c; }
                .footer {
                    margin-top: 20px;
                    padding-top: 10px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #777;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏛️ Politician Trade Alert</h1>
                    <p>Detected {count} new trade(s)</p>
                </div>
        """.format(count=len(trades))

        for trade in trades:
            transaction_class = 'buy' if 'purchase' in trade.transaction_type.lower() else 'sell'
            html += f"""
                <div class="trade-card">
                    <div class="trade-header">{trade.politician_name}</div>
                    <div class="trade-detail">
                        <span class="label">Ticker:</span>
                        <strong>{trade.ticker}</strong>
                    </div>
                    <div class="trade-detail">
                        <span class="label">Asset:</span>
                        {trade.asset_description or 'N/A'}
                    </div>
                    <div class="trade-detail">
                        <span class="label">Transaction:</span>
                        <span class="{transaction_class}">{trade.transaction_type}</span>
                    </div>
                    <div class="trade-detail">
                        <span class="label">Amount Range:</span>
                        {trade.amount_range or 'N/A'}
                    </div>
                    <div class="trade-detail">
                        <span class="label">Transaction Date:</span>
                        {trade.transaction_date.strftime('%Y-%m-%d') if trade.transaction_date else 'N/A'}
                    </div>
                    <div class="trade-detail">
                        <span class="label">Disclosure Date:</span>
                        {trade.disclosure_date.strftime('%Y-%m-%d') if trade.disclosure_date else 'N/A'}
                    </div>
                </div>
            """

        html += f"""
                <div class="footer">
                    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def test_connection(self) -> bool:
        """Test SMTP connection and credentials."""
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
            logger.info("Email connection test successful")
            return True
        except Exception as e:
            logger.error(f"Email connection test failed: {e}")
            return False
