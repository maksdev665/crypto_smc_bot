from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, BigInteger, String, Float, Boolean, DateTime, Text, JSON, ForeingKey, Enum, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from src.config.constants import SetupType, TradingSide, OrderType, PositionStatus, MarketStructure, TimeFrame
from src.database.base import Base
from src.database.models import Trade, MarketData

class TradingPair(Base):
    """Торговые пары и их настройки"""
    __tablename__ = 'trading_pairs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    base_currency: Mapped[str] = mapped_column(String(10))
    quote_currency: Mapped[str] = mapped_column(String(10))

    # Volatility metrics
    daily_volatility: Mapped[Optional[float]] = mapped_column(Float)
    weekly_volatility: Mapped[Optional[float]] = mapped_column(Float)
    average_volume: Mapped[Optional[float]] = mapped_column(Float)

    # Trading settings
    tier: Mapped[int] = mapped_column(Integer, default=2)   # 1 - high liquidity, 2 - medium
    min_trade_size: Mapped[float] = mapped_column(Float)
    max_leverage: Mapped[int] = mapped_column(Integer, default=20)
    maker_fee: Mapped[float] = mapped_column(Float, default=0.02)
    taker_fee: Mapped[float] = mapped_column(Float, default=0.05)

    # Statistics
    total_trades: Mapped[int] = mapped_column(Integer, default=0)
    win_rate: Mapped[Optional[float]] = mapped_column(Float)
    aretage_rr: Mapped[Optional[float]] = mapped_column(Float)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    trades: Mapped[List['Trade']] = relationship(back_populates='pair')
    market_data: Mapped[List['MarketData']] = relationship(back_populates='pair')
    