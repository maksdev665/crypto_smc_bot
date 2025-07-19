from datetime import datetime
from typing import Optional, List

from sqlalchemy import Integer, BigInteger, String, Float, Boolean, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from src.config.constants import SetupType, TradingSide
from src.database.base import Base
from src.database.models import Trade

class Signal(Base):
    """История сигналов"""
    __tablename__ = 'signals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trade_id: Mapped[int] = mapped_column(Integer, ForeignKey('trades.id'))

    # Signal details
    setup_type: Mapped[SetupType] = mapped_column(Enum(SetupType))
    pair_symbol: Mapped[str] = mapped_column(String(20))
    side: Mapped[TradingSide] = mapped_column(Enum(TradingSide))

    # Levels
    entry_price: Mapped[float] = mapped_column(Float)
    stop_loss: Mapped[float] = mapped_column(Float)
    take_profit: Mapped[float] = mapped_column(Float)

    # Metadata
    confluence_factor: Mapped[List[str]] = mapped_column(JSON)
    message_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    channel_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    # Validity
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    trade: Mapped[Optional['Trade']] = relationship(back_popultes='signals')