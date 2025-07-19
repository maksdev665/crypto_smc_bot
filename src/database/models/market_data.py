from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, Integer, BigInteger, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from src.config.constants import SetupType, TradingSide, OrderType, PositionStatus, MarketStructure, TimeFrame
from src.database.base import Base
from src.database.models import TradingPair

class MarketData(Base):
    """Рыночные данные для анализа"""
    __tablename__ = 'market_data'
    __table_args__ = (
        Index('idx_market_data_pair_timeframe', 'pair_id', 'timeframe', 'timestamp')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pair_id: Mapped[int] = mapped_column(Integer, ForeignKey('trading_pairs.id'))
    timeframe: Mapped[TimeFrame] = mapped_column(Enum(TimeFrame))

    # OHLCV
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
    volume: Mapped[float] = mapped_column(Float)

    # Indicators
    order_blocks: Mapped[Optional[List[dict]]] = mapped_column(JSON)
    liquidity_zones: Mapped[Optional[List[dict]]] = mapped_column(JSON)
    volume_profile: Mapped[Optional[dict]] = mapped_column(JSON)
    cvd: Mapped[Optional[float]] = mapped_column(Float)

    # Market structure
    structure: Mapped[Optional[MarketStructure]] = mapped_column(Enum(MarketStructure))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    pair: Mapped['TradingPair'] = relationship(back_populates='market_data')