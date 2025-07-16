from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, BigInteger, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from src.database.base import Base
from src.database.models import User

class BotSettings(Base):
    """Настройки бота"""
    __tablename__ = 'bot_settings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))

    # Trading settings
    is_trading_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    trading_budget: Mapped[float] = mapped_column(Float, default=100.0)
    default_leverage: Mapped[int] = mapped_column(Integer, default=10)
    risk_per_trade: Mapped[float] = mapped_column(Float, default=2.0)
    max_daily_loss: Mapped[float] = mapped_column(Float, default=5.0)
    max_concurrent_trades: Mapped[int] = mapped_column(Integer, default=3)

    # Strategy settings
    enabled_setup: Mapped[List[str]] = mapped_column(JSON, default=list)
    min_rr_ration: Mapped[float] = mapped_column(Float, default=3.0)
    confluence_factors: Mapped[int] = mapped_column(Integer, default=3)

    # Pairs settings
    enabled_pairs: Mapped[List[str]] = mapped_column(JSON, default=list)

    # Notification settings
    signal_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    send_open_notification: Mapped[bool] = mapped_column(Boolean, default=True)
    send_close_notification: Mapped[bool] = mapped_column(Boolean, default=True)
    send_daily_summery: Mapped[bool] = mapped_column(Boolean, default=True)

    # API Keys (encrypted)
    bingx_api_key_encrypted: Mapped[Optional[str]] = mapped_column(Text)
    bingx_secret_key_encrypted: Mapped[Optional[str]] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    user: Mapped['User'] = relationship(back_populates='settings')

