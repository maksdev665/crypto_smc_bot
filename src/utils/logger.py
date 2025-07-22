import sys
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

from loguru import logger

from src.config.settings import settings

def setup_logger(name: Optional[str] = None):
    """
    Настроить логгер для модуля
    
    Args:
        name: Имя модуля
        
    Returns:
        Настроенный логгер
    """
    # Удаляем стандартный обработчик
    logger.remove()

    # Создаем директорию для логов
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    # Формат логов
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Добавляем вывод в консоль
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.LOG_LEVEL,
        colorize=True,
        backtrace=True,
        diagnose=True
    )

    # Добавляем запись в файл
    logger.add(
        settings.LOG_FILE,
        format=log_format,
        lever=settings.LOG_LEVEL,
        rotation='500 MB',
        retention='1 week',
        compression='zip',
        backtrace=True,
        diagnose=True,
        enqueue=True
    )

    # Добавляем отдельный файл для ошибок
    logger.add(
        'logs/error.log',
        format=log_format,
        lever='ERROR',
        rotation='100 MB',
        retention='1 month',
        compression='zip',
        backtrace=True,
        diagnose=True,
        enqueue=True
    )

    # Добавляем файл для торговых операций
    logger.add(
        'logs/trading.log',
        format=log_format,
        lever='INFO',
        filter=lambda record: 'trading' in record['extra'],
        rotation='1 day',
        retention='1 month',
        compression='zip',
        enqueue=True
    )

    # Интеграция с стандартным logging
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Получаем соответствующий уровень Loguru
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Находим вызывающий фрейм
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            
            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Настраиваем перехват логов от других библиотек
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Отключаем некоторые шумные логгеры
    for logger_name in ['aiogram.event', 'aiohttp.access', 'asyncio']:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    # Если указано имя модуля, добавляем его в контекст
    if name:
        return logger.bind(name=name)
    
    return logger

def log_trade_action(action: str, **kwargs):
    """
    Логировать торговое действие
    
    Args:
        action: Тип действия
        **kwargs: Дополнительные параметры
    """
    logger.bind(trading=True).info(
        f'Trade action: {action}',
        extra={
            'action': action,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
    )

def log_error_with_context(error: Exception, context: dict):
    """
    Логировать ошибку с контекстом
    
    Args:
        error: Исключение
        context: Контекст ошибки
    """
    logger.error(
        f'Error occurred: {type(error).__name__}: {str(error)}',
        exc_info=True,
        extra=context
    )

def log_performance_metric(metric_name: str, value: float, unit: str = 'ms'):
    """
    Логировать метрику производительности
    
    Args:
        metric_name: Название метрики
        value: Значение
        unit: Единица измерения
    """
    logger.debug(
        f'Performance metric: {metric_name} = {value:.2f} {unit}',
        extra={
            'metric': metric_name,
            'value': value,
            'unit': unit,
            'timestamp': datetime.now().isoformat()
        }
    )


class LogContext:
    """Контекстный менеджер для логирования с дополнительным контекстом"""
    def __init__(self, **kwargs):
        self.context = kwargs
        self.logger_context = None

    def __enter__(self):
        self.logger_context = logger.contextualize(**self.context)
        return self.logger_context.__enter__()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.logger_context:
            self.logger_context.__exit__(exc_type, exc_val, exc_tb)

# Экспортируем настроки логгера
default_logger = setup_logger()