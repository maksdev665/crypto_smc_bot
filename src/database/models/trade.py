from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, Integer, BigInteger, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from src.config.constants import SetupType, TradingSide, PositionStatus, MarketStructure, TimeFrame
from src.database.base import Base
from src.database.models import User, TradingPair, Signal

class Trade(Base):
    """Сделки"""
    __tablename__ = 'trades'
    __table_args__ = (
        Index('idx_trades_user_created', 'user_id', 'created_at'),
        Index('idx_trades_status', 'status')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))
    pair_id: Mapped[int] = mapped_column(Integer, ForeignKey('trading_pairs.id'))

    # Trading details
    status_type: Mapped[SetupType] = mapped_column(Enum(SetupType))
    side: Mapped[TradingSide] = mapped_column(Enum(TradingSide))
    status: Mapped[PositionStatus] = mapped_column(Enum())

    # Entry
    entry_price: Mapped[float] = mapped_column(Float)
    stop_loss: Mapped[float] = mapped_column(Float)
    take_profit: Mapped[float] = mapped_column(Float)
    position_size: Mapped[float] = mapped_column(Float)
    leverage: Mapped[int] = mapped_column(Integer)

    # Risk management
    risk_amount: Mapped[float] = mapped_column(Float)
    risk_percent: Mapped[float] = mapped_column(Float)
    rr_ratio: Mapped[float] = mapped_column(Float)

    # Exit
    exit_price: Mapped[Optional[float]] = mapped_column(Float)
    exit_reason: Mapped[Optional[str]] = mapped_column(String(50))

    # Result
    pnl_amoun: Mapped[Optional[float]] = mapped_column(Float)
    pnl_percent: Mapped[Optional[float]] = mapped_column(Float)
    commision: Mapped[Optional[float]] = mapped_column(Float)

    # Confluence factor
    confluence_factor: Mapped[List[str]] = mapped_column(JSON)
    confluence_score: Mapped[int] = mapped_column(Integer)

    # Order IDs
    entry_order_id: Mapped[Optional[str]] = mapped_column(String(100))
    stop_order_id: Mapped[Optional[str]] = mapped_column(String(100))
    tp_order_id: Mapped[Optional[str]] = mapped_column(String(100))

    # Timestamp
    signal_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    entry_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    exit_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Analysis data
    analysis_data: Mapped[Optional[dict]] = mapped_column(JSON)     # Сохраняем данные анализа

    # Relationships
    user: Mapped['User'] = relationship(back_populates='trades')
    pair: Mapped['TradingPair'] = relationship(back_populates='trades')
    signals: Mapped[List['Signal']] = relationship(back_populates='trades')
    

