"""Hyper - A professional Python project with testing and CI/CD."""

__version__ = "0.1.0"
__author__ = "mnareerizoh"

from hyper.core import greet
from hyper.data_analysis import (
    calculate_bollinger_bands,
    calculate_cumulative_returns,
    calculate_exponential_moving_average,
    calculate_max_drawdown,
    calculate_mean,
    calculate_median,
    calculate_profit_factor,
    calculate_returns,
    calculate_rsi,
    calculate_sharpe_ratio,
    calculate_simple_moving_average,
    calculate_std_dev,
    calculate_volatility,
    calculate_win_rate,
)
from hyper.trading_bot import (
    Order,
    OrderStatus,
    OrderType,
    Position,
    TradingBot,
    TradeSignal,
)

__all__ = [
    # Core
    "greet",
    # Data Analysis
    "calculate_mean",
    "calculate_median",
    "calculate_std_dev",
    "calculate_simple_moving_average",
    "calculate_exponential_moving_average",
    "calculate_volatility",
    "calculate_rsi",
    "calculate_bollinger_bands",
    "calculate_returns",
    "calculate_cumulative_returns",
    "calculate_sharpe_ratio",
    "calculate_max_drawdown",
    "calculate_win_rate",
    "calculate_profit_factor",
    # Trading Bot
    "Order",
    "OrderStatus",
    "OrderType",
    "Position",
    "TradingBot",
    "TradeSignal",
]
