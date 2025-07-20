from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, BigInteger, String, Float, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.database.base import Base

class Statistics(Base):
    """Статистика торговли"""
    __tablename__ = 'statistics'
    __table_args__ = (
        Index('idx_statistics_user_period', 'user_id', 'period_type', 'period_start')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))

    # Period
    period_type: Mapped[str] = mapped_column(String(20))  # daily, weekly, monthly, all_time
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    period_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Metrics
    total_trades: Mapped[int] = mapped_column(Integer, default=0)
    winning_trades: Mapped[int] = mapped_column(Integer, default=0)
    losing_trades: Mapped[int] = mapped_column(Integer, default=0)

    # Financial
    total_pnl: Mapped[float] = mapped_column(Float, default=0.0)
    total_commision: Mapped[float] = mapped_column(Float, default=0.0)
    max_wind: Mapped[Optional[float]] = mapped_column(Float)
    max_loss: Mapped[Optional[float]] = mapped_column(Float)
    average_win: Mapped[Optional[float]] = mapped_column(Float)
    average_loss: Mapped[Optional[float]] = mapped_column(Float)

    # Ratios
    win_rate: Mapped[Optional[float]] = mapped_column(Float)
    profit_factor: Mapped[Optional[float]] = mapped_column(Float)
    average_rr: Mapped[Optional[float]] = mapped_column(Float)
    sharpe_ratio: Mapped[Optional[float]] = mapped_column(Float)

    # Drawdown
    max_drawdown: Mapped[Optional[float]] = mapped_column(Float)
    max_drawdown_duration: Mapped[Optional[int]] = mapped_column(Integer)  # в часах

    # By setup type
    stats_by_setup: Mapped[Optional[dict]] = mapped_column(JSON)

    # By pairs
    stats_by_pair: Mapped[Optional[dict]] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )