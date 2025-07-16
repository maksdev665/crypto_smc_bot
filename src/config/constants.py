"""
Константы для торговой стратегии Smart Money Concepts
"""
from enum import Enum
from typing import Dict, Tuple


class TimeFrame(str, Enum):
    """Временные интервалы для анализа"""
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"


class TradingSide(str, Enum):
    """Направление сделки"""
    LONG = "long"
    SHORT = "short"


class SetupType(str, Enum):
    """Типы торговых сетапов"""
    ORDER_BLOCK_REVERSAL = "order_block_reversal"
    LIQUIDITY_GRAB = "liquidity_grab"
    POC_BOUNCE = "poc_bounce"


class MarketStructure(str, Enum):
    """Структура рынка"""
    BULLISH_TREND = "bullish_trend"
    BEARISH_TREND = "bearish_trend"
    CONSOLIDATION = "consolidation"
    UNDEFINED = "undefined"


class OrderType(str, Enum):
    """Типы ордеров"""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"


class PositionStatus(str, Enum):
    """Статус позиции"""
    PENDING = "pending"
    OPEN = "open"
    PARTIAL_CLOSED = "partial_closed"
    CLOSED = "closed"
    CANCELLED = "cancelled"


# Risk/Reward соотношения для каждого сетапа
RR_RATIOS: Dict[SetupType, float] = {
    SetupType.ORDER_BLOCK_REVERSAL: 4.0,
    SetupType.LIQUIDITY_GRAB: 5.0,
    SetupType.POC_BOUNCE: 3.0
}

# Минимальные факторы confluence для каждого сетапа
MIN_CONFLUENCE_FACTORS: Dict[SetupType, int] = {
    SetupType.ORDER_BLOCK_REVERSAL: 3,
    SetupType.LIQUIDITY_GRAB: 4,
    SetupType.POC_BOUNCE: 3
}

# Размеры стопов для разных типов активов (в процентах)
STOP_LOSS_PERCENTAGES: Dict[str, Tuple[float, float]] = {
    "BTC": (2.0, 3.0),
    "ETH": (2.0, 3.0),
    "major_alts": (4.0, 6.0),
    "small_caps": (8.0, 12.0),
    "meme_coins": (15.0, 20.0)
}

# Множители плеча в зависимости от волатильности
LEVERAGE_MULTIPLIERS: Dict[str, int] = {
    "low_volatility": 20,
    "medium_volatility": 15,
    "high_volatility": 10,
    "extreme_volatility": 5
}

# Временные зоны для анализа ликвидности
LIQUIDITY_TIME_ZONES = {
    "asian_session": (0, 8),      # UTC время
    "european_session": (7, 16),
    "us_session": (13, 22),
    "overlap_eu_us": (13, 16)
}

# Параметры Volume Profile
VOLUME_PROFILE_SETTINGS = {
    "value_area_percentage": 70,  # Процент объема для Value Area
    "min_node_size": 100,         # Минимальный размер узла
    "profile_periods": {
        TimeFrame.M15: 96,        # 24 часа для 15-минутного графика
        TimeFrame.H1: 24,         # 24 часа для часового графика
        TimeFrame.H4: 28,         # 7 дней для 4-часового графика
    }
}

# Параметры CVD (Cumulative Volume Delta)
CVD_SETTINGS = {
    "divergence_threshold": 0.15,  # Порог для определения дивергенции
    "absorption_volume": 1000,     # Минимальный объем для absorption
    "reset_period": 24,           # Часы для сброса CVD
}

# Параметры Order Flow
ORDER_FLOW_SETTINGS = {
    "imbalance_ratio": 3.0,       # Соотношение для imbalance
    "large_order_threshold": 100,  # BTC эквивалент для large orders
    "footprint_rows": 20,         # Количество строк в footprint
}

# Настройки риск-менеджмента
RISK_MANAGEMENT = {
    "max_concurrent_trades": 3,
    "max_risk_per_trade": 2.0,    # Процент от депозита
    "max_daily_trades": 5,
    "max_daily_loss": 5.0,        # Процент от депозита
    "max_weekly_drawdown": 15.0,
    "partial_close_targets": [1.0, 2.0],  # R-ratios для частичного закрытия
    "partial_close_percentages": [50, 30],  # Проценты позиции для закрытия
    "breakeven_level": 1.5,       # R-ratio для переноса стопа в безубыток
}

# Фильтры качества сделок
TRADE_QUALITY_FILTERS = {
    "min_winrate": 55.0,          # Минимальный winrate для сетапа
    "min_sample_size": 20,        # Минимальное количество сделок для статистики
    "confidence_interval": 0.95,   # Доверительный интервал
}

# Эмодзи для уведомлений
EMOJI = {
    "long": "🟢",
    "short": "🔴",
    "win": "✅",
    "loss": "❌",
    "breakeven": "🔸",
    "warning": "⚠️",
    "info": "ℹ️",
    "chart": "📊",
    "money": "💰",
    "target": "🎯",
    "stop": "🛑",
    "entry": "🚀",
    "analysis": "🔍",
    "settings": "⚙️",
    "statistics": "📈",
}

# Форматы сообщений
MESSAGE_TEMPLATES = {
    "signal": """
{emoji} **{setup_type} Signal**

**Pair:** {pair}
**Side:** {side}
**Entry:** {entry}
**Stop Loss:** {stop_loss} ({stop_percent}%)
**Take Profit:** {take_profit} ({rr_ratio}R)

**Confluence Factors:**
{factors}

**Risk:** {risk_amount} USDT ({risk_percent}% of account)
**Position Size:** {position_size} {base_currency}
**Leverage:** {leverage}x

⏰ Valid until: {valid_until}
""",
    
    "trade_open": """
{emoji} **Trade Opened**

**Pair:** {pair}
**Side:** {side}
**Entry Price:** {entry_price}
**Position Size:** {position_size}
**Risk:** {risk_amount} USDT
""",
    
    "trade_closed": """
{emoji} **Trade Closed**

**Pair:** {pair}
**Result:** {result}
**PnL:** {pnl} USDT ({pnl_percent}%)
**Duration:** {duration}
**Exit Price:** {exit_price}
""",
    
    "daily_summary": """
📊 **Daily Trading Summary**

**Date:** {date}
**Trades:** {total_trades}
**Win Rate:** {winrate}%
**Total PnL:** {total_pnl} USDT ({pnl_percent}%)

**Best Trade:** {best_trade}
**Worst Trade:** {worst_trade}
**Average RR:** {avg_rr}

**Account Balance:** {balance} USDT
"""
}