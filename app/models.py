"""Database models for tracking politician trades."""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Trade(Base):
    """Model for storing politician trade records."""

    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    politician_name = Column(String, nullable=False, index=True)
    transaction_date = Column(DateTime, nullable=False)
    disclosure_date = Column(DateTime, nullable=False)
    ticker = Column(String, nullable=False, index=True)
    asset_description = Column(String)
    asset_type = Column(String)
    transaction_type = Column(String, nullable=False)  # Purchase, Sale, Exchange
    amount_range = Column(String)  # e.g., "$1,001 - $15,000"
    amount_min = Column(Float)
    amount_max = Column(Float)
    comment = Column(String)
    notified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Trade(politician='{self.politician_name}', ticker='{self.ticker}', type='{self.transaction_type}')>"


class Database:
    """Database management class."""

    def __init__(self, db_path='sqlite:///data/trades.db'):
        """Initialize database connection."""
        self.engine = create_engine(db_path, echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_trade(self, trade_data):
        """Add a new trade to the database."""
        trade = Trade(**trade_data)
        self.session.add(trade)
        self.session.commit()
        return trade

    def get_unnotified_trades(self):
        """Get all trades that haven't been notified yet."""
        return self.session.query(Trade).filter_by(notified=False).all()

    def mark_as_notified(self, trade_id):
        """Mark a trade as notified."""
        trade = self.session.query(Trade).filter_by(id=trade_id).first()
        if trade:
            trade.notified = True
            self.session.commit()

    def trade_exists(self, politician_name, ticker, transaction_date, transaction_type):
        """Check if a trade already exists in the database."""
        existing = self.session.query(Trade).filter_by(
            politician_name=politician_name,
            ticker=ticker,
            transaction_date=transaction_date,
            transaction_type=transaction_type
        ).first()
        return existing is not None

    def get_recent_trades(self, politician_name=None, days=30):
        """Get recent trades, optionally filtered by politician."""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        query = self.session.query(Trade).filter(Trade.disclosure_date >= cutoff_date)
        if politician_name:
            query = query.filter_by(politician_name=politician_name)

        return query.order_by(Trade.disclosure_date.desc()).all()

    def close(self):
        """Close database connection."""
        self.session.close()
