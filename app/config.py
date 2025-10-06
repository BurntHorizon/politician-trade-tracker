"""Configuration management for the politician trade tracker."""

import os
import yaml
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""

    def __init__(self, config_path='config.yaml'):
        """Initialize configuration from YAML file and environment variables."""
        self.config_path = config_path
        self._load_config()
        self._load_env_vars()

    def _load_config(self):
        """Load configuration from YAML file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            # Default configuration
            self.config = {
                'politicians': ['Nancy Pelosi'],
                'check_interval_minutes': 60,
                'email': {
                    'enabled': True,
                    'subject_prefix': '[Politician Trade Alert]'
                },
                'data_source': {
                    'type': 'senate_stock_watcher',
                    'url': 'https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_transactions.json'
                }
            }

    def _load_env_vars(self):
        """Load sensitive configuration from environment variables."""
        # Email configuration
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.email_from = os.getenv('EMAIL_FROM', self.smtp_username)
        self.email_to = os.getenv('EMAIL_TO', '')

        # Database configuration
        self.database_path = os.getenv('DATABASE_PATH', 'sqlite:///data/trades.db')

        # Application configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')

    @property
    def politicians(self) -> List[str]:
        """Get list of politicians to track."""
        return self.config.get('politicians', [])

    @property
    def check_interval_minutes(self) -> int:
        """Get check interval in minutes."""
        return self.config.get('check_interval_minutes', 60)

    @property
    def email_enabled(self) -> bool:
        """Check if email notifications are enabled."""
        return self.config.get('email', {}).get('enabled', True)

    @property
    def email_subject_prefix(self) -> str:
        """Get email subject prefix."""
        return self.config.get('email', {}).get('subject_prefix', '[Politician Trade Alert]')

    @property
    def data_source_type(self) -> str:
        """Get data source type."""
        return self.config.get('data_source', {}).get('type', 'senate_stock_watcher')

    @property
    def data_source_url(self) -> str:
        """Get data source URL."""
        return self.config.get('data_source', {}).get('url',
            'https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_transactions.json')

    def validate(self) -> tuple[bool, List[str]]:
        """Validate configuration."""
        errors = []

        if not self.politicians:
            errors.append("No politicians configured to track")

        if self.email_enabled:
            if not self.smtp_username:
                errors.append("SMTP_USERNAME not set")
            if not self.smtp_password:
                errors.append("SMTP_PASSWORD not set")
            if not self.email_to:
                errors.append("EMAIL_TO not set")

        return len(errors) == 0, errors

    def __repr__(self):
        """String representation of config."""
        return f"<Config(politicians={len(self.politicians)}, interval={self.check_interval_minutes}min)>"
