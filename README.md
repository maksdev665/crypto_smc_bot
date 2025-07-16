# crypto_smc_bot
Telegram bot for Crypto

# Структура проекта Smart Money Trading Bot

```
crypto_smc_bot/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic.ini
├── README.md
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── constants.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── settings.py
│   │   │   ├── trade.py
│   │   │   ├── signal.py
│   │   │   └── statistics.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── user_repo.py
│   │       ├── settings_repo.py
│   │       ├── trade_repo.py
│   │       └── statistics_repo.py
│   │
│   ├── exchange/
│   │   ├── __init__.py
│   │   ├── bingx_client.py
│   │   ├── order_manager.py
│   │   └── exceptions.py
│   │
│   ├── strategy/
│   │   ├── __init__.py
│   │   ├── base_strategy.py
│   │   ├── smc_strategy.py
│   │   ├── indicators/
│   │   │   ├── __init__.py
│   │   │   ├── order_blocks.py
│   │   │   ├── liquidity_zones.py
│   │   │   ├── volume_profile.py
│   │   │   └── cvd.py
│   │   ├── setups/
│   │   │   ├── __init__.py
│   │   │   ├── order_block_reversal.py
│   │   │   ├── liquidity_grab.py
│   │   │   └── poc_bounce.py
│   │   └── risk_management.py
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── market_analyzer.py
│   │   ├── order_flow.py
│   │   └── statistics_calculator.py
│   │
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── create_bot.py
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── settings.py
│   │   │   ├── trading.py
│   │   │   ├── statistics.py
│   │   │   └── errors.py
│   │   ├── keyboards/
│   │   │   ├── __init__.py
│   │   │   ├── main_menu.py
│   │   │   ├── settings_kb.py
│   │   │   ├── trading_kb.py
│   │   │   └── inline_kb.py
│   │   ├── middlewares/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── throttling.py
│   │   ├── states/
│   │   │   ├── __init__.py
│   │   │   ├── settings_states.py
│   │   │   └── trading_states.py
│   │   └── filters/
│   │       ├── __init__.py
│   │       └── admin.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── trading_service.py
│   │   ├── signal_service.py
│   │   ├── notification_service.py
│   │   └── statistics_service.py
│   │
│   ├── scheduler/
│   │   ├── __init__.py
│   │   ├── trading_scheduler.py
│   │   └── tasks.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       ├── formatters.py
│       ├── validators.py
│       └── decorators.py
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_strategy/
    ├── test_exchange/
    └── test_bot/
```

## Описание модулей

### config/
- **settings.py** - конфигурация приложения через Pydantic Settings
- **constants.py** - константы стратегии (R:R ratios, риски, временные интервалы)

### database/
- **models/** - SQLAlchemy модели для хранения данных
- **repositories/** - паттерн Repository для работы с БД

### exchange/
- **bingx_client.py** - асинхронный клиент для BingX API
- **order_manager.py** - управление ордерами и позициями

### strategy/
- **smc_strategy.py** - реализация Smart Money Concepts стратегии
- **indicators/** - индикаторы для анализа (Order Blocks, CVD, Volume Profile)
- **setups/** - конкретные торговые сетапы из ТЗ
- **risk_management.py** - управление рисками и расчет позиций

### analysis/
- **market_analyzer.py** - анализ рыночной структуры
- **order_flow.py** - анализ потока ордеров
- **statistics_calculator.py** - расчет статистики (winrate, PnL, Sharpe ratio)

### bot/
- **handlers/** - обработчики команд бота
- **keyboards/** - клавиатуры для интерфейса
- **middlewares/** - middleware для авторизации и throttling
- **states/** - FSM состояния для настроек

### services/
- **trading_service.py** - бизнес-логика торговли
- **signal_service.py** - отправка сигналов в канал
- **notification_service.py** - уведомления администратору

### scheduler/
- **trading_scheduler.py** - планировщик для анализа рынка
- **tasks.py** - фоновые задачи
