from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Основные настройки приложения"""

    # Bot settings
    BOT_TOKEN: str = Field(..., env='BOT_TOKEN')
    ADMIN_IDS: List[int] = Field(..., env='ADMIN_IDS')

    # Database 
    DB_HOST: str = Field('localhost', env='DB_HOST')
    DB_PORT: int = Field(5432, env='DB_PORT')
    DB_NAME: str = Field('crypto_db', env='DB_NAME')
    DB_USER: str = Field('admin', env='DB_USER')
    DB_PASSWORD: str = Field(..., env='DB_PASSWORD')

    # BingX API
    BINGX_API_KEY: str = Field(..., env='BINGX_API_KEY')
    BINGX_SECRET_KEY: str = Field(..., env='BINGX_SECRET_KEY')
    BINGX_BASE_URL: str = Field('https://open-api.bingx.com', env='BINGX_BASE_URL')

    # Trading settings
    DEFAULT_LEVERAGE: int = Field(10, env='DEFAULT_LEGERAGE')
    MAX_LEVERAGE: int = Field(20, env='MAX_LEVERAGE')
    DEFAULT_RISK_PERCENT: float = Field(2.0, env='DEFAULT_RISK_PERCENT')
    MAX_DAILY_LOSS_PERCENT: float = Field(5.0, env='MAX_DAILY_LOSS_PERCENT')
    MAX_WEEKLY_DRAWDOWN: float = Field(15.0, env='MAX_WEEKLY_DRAWDOWN')

    # Strategy settings
    MIN_RR_RATION: float = Field(3.0, env='MIN_RR_RATION')
    TARGET_WINRATE: float = Field(55.0, env='TARGET_WINRATE')
    MAX_TRADES_PER_DAY: int = Field(5, env='MAX_TRADES_PER_DAY')
    CONFLUENCE_MIN_FACTORS: int = Field(3, env='CONFLUENCE_MIN_FACTORS')

    # Analysis interval
    ANALYSIS_INTERVALS: List[str] = Field(
        default=['5m', '15m', '1h', '4h'],
        env='ANALYSIS_INTERVALS'
    )

    # Telegram settings
    SIGNAL_CHANNEL_ID: Optional[int] = Field(None, env='SIGNAL_CHANNEL_ID')
    LOG_CHANNEL_ID: Optional[int] = Field(None, env='LOG_CHANNEL_ID')

    # Logging
    LOG_LEVEL: str = Field('INFO', env='LOG_LEVEL')
    LOG_FILE: str = Field('logs/trading_bot.log', env='LOG_FILE')

    # Scheduler settings
    MARKET_ANALYSIS_INTERVAL: int = Field(60, 'MARKET_ANALYSIS_INTERVAL') # seconds
    STATISTICS_UPDATE_INTERVAL: int = Field(300, 'STATISTICS_UPDATE_INTERVAL') # seconds

    @field_validator('ADMIN_IDS', mode='before')
    @classmethod
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            return [int(id.strip()) for id in v.split(',')]
        return v
    
    @field_validator('ANALYSIS_INTERVALS', mode='before')
    @classmethod
    def parse_intervals(cls, v):
        if isinstance(v, str):
            return [interval.strip() for interval in v.split(',')]
        return v

    @property
    def database_url(self) -> str:
        """Получить URL для подключения к БД"""
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    class Config:
        env_file = '.env'
        env_file_encode = 'utf-8'
        case_sensitive = True


settings = Settings()

