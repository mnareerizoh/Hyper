"""Tests for hyper.trading_bot module."""

import pytest
from hyper.trading_bot import (
    Order,
    OrderStatus,
    OrderType,
    Position,
    TradeSignal,
    TradingBot,
)


class TestOrderType:
    """Tests for OrderType enum."""

    def test_order_type_buy(self) -> None:
        """Test BUY order type."""
        assert OrderType.BUY.value == "BUY"

    def test_order_type_sell(self) -> None:
        """Test SELL order type."""
        assert OrderType.SELL.value == "SELL"


class TestOrderStatus:
    """Tests for OrderStatus enum."""

    def test_order_status_pending(self) -> None:
        """Test PENDING status."""
        assert OrderStatus.PENDING.value == "PENDING"

    def test_order_status_filled(self) -> None:
        """Test FILLED status."""
        assert OrderStatus.FILLED.value == "FILLED"


class TestTradeSignal:
    """Tests for TradeSignal enum."""

    def test_trade_signal_buy(self) -> None:
        """Test BUY signal."""
        assert TradeSignal.BUY.value == "BUY"

    def test_trade_signal_hold(self) -> None:
        """Test HOLD signal."""
        assert TradeSignal.HOLD.value == "HOLD"


class TestOrder:
    """Tests for Order dataclass."""

    def test_order_creation(self) -> None:
        """Test order creation."""
        order = Order(
            order_id=1,
            order_type=OrderType.BUY,
            symbol="EUR/USD",
            quantity=1.0,
            price=1.10,
            status=OrderStatus.PENDING,
        )
        assert order.order_id == 1
        assert order.symbol == "EUR/USD"

    def test_calculate_profit_loss_buy(self) -> None:
        """Test profit/loss calculation for BUY order."""
        order = Order(
            order_id=1,
            order_type=OrderType.BUY,
            symbol="EUR/USD",
            quantity=1.0,
            price=1.10,
            status=OrderStatus.FILLED,
            entry_price=1.10,
            exit_price=1.12,
        )
        pnl = order.calculate_profit_loss()
        assert pnl == pytest.approx(0.02)

    def test_calculate_profit_loss_sell(self) -> None:
        """Test profit/loss calculation for SELL order."""
        order = Order(
            order_id=1,
            order_type=OrderType.SELL,
            symbol="EUR/USD",
            quantity=1.0,
            price=1.10,
            status=OrderStatus.FILLED,
            entry_price=1.12,
            exit_price=1.10,
        )
        pnl = order.calculate_profit_loss()
        assert pnl == pytest.approx(0.02)

    def test_calculate_profit_loss_missing_prices(self) -> None:
        """Test profit/loss calculation with missing prices."""
        order = Order(
            order_id=1,
            order_type=OrderType.BUY,
            symbol="EUR/USD",
            quantity=1.0,
            price=1.10,
            status=OrderStatus.PENDING,
        )
        with pytest.raises(ValueError):
            order.calculate_profit_loss()

    def test_calculate_profit_loss_percentage(self) -> None:
        """Test profit/loss percentage calculation."""
        order = Order(
            order_id=1,
            order_type=OrderType.BUY,
            symbol="EUR/USD",
            quantity=1.0,
            price=1.10,
            status=OrderStatus.FILLED,
            entry_price=100.0,
            exit_price=110.0,
        )
        percentage = order.calculate_profit_loss_percentage()
        assert percentage == pytest.approx(10.0)


class TestPosition:
    """Tests for Position dataclass."""

    def test_position_creation(self) -> None:
        """Test position creation."""
        position = Position(
            position_id=1,
            symbol="EUR/USD",
            quantity=1.0,
            entry_price=1.10,
            entry_time=0,
            order_type=OrderType.BUY,
        )
        assert position.position_id == 1
        assert position.symbol == "EUR/USD"

    def test_is_stop_loss_triggered_buy(self) -> None:
        """Test stop loss trigger for BUY position."""
        position = Position(
            position_id=1,
            symbol="EUR/USD",
            quantity=1.0,
            entry_price=1.10,
            entry_time=0,
            order_type=OrderType.BUY,
            stop_loss=1.08,
        )
        assert not position.is_stop_loss_triggered(1.09)
        assert position.is_stop_loss_triggered(1.08)
        assert position.is_stop_loss_triggered(1.07)

    def test_is_stop_loss_triggered_sell(self) -> None:
        """Test stop loss trigger for SELL position."""
        position = Position(
            position_id=1,
            symbol="EUR/USD",
            quantity=1.0,
            entry_price=1.10,
            entry_time=0,
            order_type=OrderType.SELL,
            stop_loss=1.12,
        )
        assert not position.is_stop_loss_triggered(1.11)
        assert position.is_stop_loss_triggered(1.12)

    def test_is_take_profit_triggered_buy(self) -> None:
        """Test take profit trigger for BUY position."""
        position = Position(
            position_id=1,
            symbol="EUR/USD",
            quantity=1.0,
            entry_price=1.10,
            entry_time=0,
            order_type=OrderType.BUY,
            take_profit=1.15,
        )
        assert not position.is_take_profit_triggered(1.14)
        assert position.is_take_profit_triggered(1.15)

    def test_is_take_profit_triggered_sell(self) -> None:
        """Test take profit trigger for SELL position."""
        position = Position(
            position_id=1,
            symbol="EUR/USD",
            quantity=1.0,
            entry_price=1.10,
            entry_time=0,
            order_type=OrderType.SELL,
            take_profit=1.05,
        )
        assert not position.is_take_profit_triggered(1.06)
        assert position.is_take_profit_triggered(1.05)

    def test_calculate_unrealized_pnl_buy(self) -> None:
        """Test unrealized P&L for BUY position."""
        position = Position(
            position_id=1,
            symbol="EUR/USD",
            quantity=1.0,
            entry_price=100.0,
            entry_time=0,
            order_type=OrderType.BUY,
        )
        pnl = position.calculate_unrealized_pnl(110.0)
        assert pnl == pytest.approx(10.0)

    def test_calculate_unrealized_pnl_sell(self) -> None:
        """Test unrealized P&L for SELL position."""
        position = Position(
            position_id=1,
            symbol="EUR/USD",
            quantity=1.0,
            entry_price=100.0,
            entry_time=0,
            order_type=OrderType.SELL,
        )
        pnl = position.calculate_unrealized_pnl(90.0)
        assert pnl == pytest.approx(10.0)

    def test_calculate_unrealized_pnl_percentage(self) -> None:
        """Test unrealized P&L percentage."""
        position = Position(
            position_id=1,
            symbol="EUR/USD",
            quantity=1.0,
            entry_price=100.0,
            entry_time=0,
            order_type=OrderType.BUY,
        )
        percentage = position.calculate_unrealized_pnl_percentage(110.0)
        assert percentage == pytest.approx(10.0)


class TestTradingBot:
    """Tests for TradingBot class."""

    def test_bot_initialization(self) -> None:
        """Test bot initialization."""
        bot = TradingBot(initial_balance=10000.0)
        assert bot.initial_balance == 10000.0
        assert bot.current_balance == 10000.0
        assert bot.risk_per_trade == 1.0

    def test_bot_initialization_invalid_balance(self) -> None:
        """Test bot initialization with invalid balance."""
        with pytest.raises(ValueError):
            TradingBot(initial_balance=-1000.0)

    def test_bot_initialization_invalid_risk(self) -> None:
        """Test bot initialization with invalid risk."""
        with pytest.raises(ValueError):
            TradingBot(initial_balance=1000.0, risk_per_trade=-1.0)

    def test_get_position_size(self) -> None:
        """Test position size calculation."""
        bot = TradingBot(initial_balance=10000.0, risk_per_trade=2.0)
        position_size = bot.get_position_size(stop_loss_distance=50.0)
        # Risk = 10000 * 0.02 = 200, Position size = 200 / 50 = 4
        assert position_size == pytest.approx(4.0)

    def test_get_position_size_invalid_distance(self) -> None:
        """Test position size with invalid stop loss distance."""
        bot = TradingBot(initial_balance=10000.0)
        with pytest.raises(ValueError):
            bot.get_position_size(stop_loss_distance=-10.0)

    def test_open_position(self) -> None:
        """Test opening a position."""
        bot = TradingBot(initial_balance=10000.0)
        position = bot.open_position(
            symbol="EUR/USD",
            order_type=OrderType.BUY,
            quantity=1.0,
            entry_price=1.10,
        )
        assert position.position_id == 1
        assert len(bot.positions) == 1

    def test_open_position_invalid_quantity(self) -> None:
        """Test opening position with invalid quantity."""
        bot = TradingBot(initial_balance=10000.0)
        with pytest.raises(ValueError):
            bot.open_position(
                symbol="EUR/USD",
                order_type=OrderType.BUY,
                quantity=-1.0,
                entry_price=1.10,
            )

    def test_open_position_max_positions(self) -> None:
        """Test opening position with max positions reached."""
        bot = TradingBot(initial_balance=10000.0, max_positions=2)
        bot.open_position(
            symbol="EUR/USD", order_type=OrderType.BUY, quantity=1.0, entry_price=1.10
        )
        bot.open_position(
            symbol="GBP/USD", order_type=OrderType.BUY, quantity=1.0, entry_price=1.35
        )
        with pytest.raises(ValueError):
            bot.open_position(
                symbol="USD/JPY",
                order_type=OrderType.BUY,
                quantity=1.0,
                entry_price=110.0,
            )

    def test_close_position(self) -> None:
        """Test closing a position."""
        bot = TradingBot(initial_balance=10000.0)
        position = bot.open_position(
            symbol="EUR/USD",
            order_type=OrderType.BUY,
            quantity=1.0,
            entry_price=100.0,
        )
        order = bot.close_position(position.position_id, exit_price=110.0)
        assert order.profit_loss == pytest.approx(10.0)
        assert len(bot.positions) == 0
        assert len(bot.closed_orders) == 1
        assert bot.current_balance == pytest.approx(10010.0)

    def test_close_position_not_found(self) -> None:
        """Test closing non-existent position."""
        bot = TradingBot(initial_balance=10000.0)
        with pytest.raises(ValueError):
            bot.close_position(position_id=999, exit_price=1.10)

    def test_get_open_positions(self) -> None:
        """Test getting open positions."""
        bot = TradingBot(initial_balance=10000.0)
        bot.open_position(
            symbol="EUR/USD", order_type=OrderType.BUY, quantity=1.0, entry_price=1.10
        )
        positions = bot.get_open_positions()
        assert len(positions) == 1

    def test_get_closed_orders(self) -> None:
        """Test getting closed orders."""
        bot = TradingBot(initial_balance=10000.0)
        position = bot.open_position(
            symbol="EUR/USD",
            order_type=OrderType.BUY,
            quantity=1.0,
            entry_price=100.0,
        )
        bot.close_position(position.position_id, exit_price=110.0)
        orders = bot.get_closed_orders()
        assert len(orders) == 1

    def test_get_total_profit_loss(self) -> None:
        """Test total profit/loss calculation."""
        bot = TradingBot(initial_balance=10000.0)
        position1 = bot.open_position(
            symbol="EUR/USD",
            order_type=OrderType.BUY,
            quantity=1.0,
            entry_price=100.0,
        )
        bot.close_position(position1.position_id, exit_price=110.0)

        position2 = bot.open_position(
            symbol="GBP/USD",
            order_type=OrderType.BUY,
            quantity=1.0,
            entry_price=100.0,
        )
        bot.close_position(position2.position_id, exit_price=105.0)

        total_pnl = bot.get_total_profit_loss()
        assert total_pnl == pytest.approx(15.0)

    def test_get_win_rate(self) -> None:
        """Test win rate calculation."""
        bot = TradingBot(initial_balance=10000.0)
        # Winning trade
        position1 = bot.open_position(
            symbol="EUR/USD",
            order_type=OrderType.BUY,
            quantity=1.0,
            entry_price=100.0,
        )
        bot.close_position(position1.position_id, exit_price=110.0)

        # Losing trade
        position2 = bot.open_position(
            symbol="GBP/USD",
            order_type=OrderType.BUY,
            quantity=1.0,
            entry_price=100.0,
        )
        bot.close_position(position2.position_id, exit_price=95.0)

        win_rate = bot.get_win_rate()
        assert win_rate == pytest.approx(50.0)

    def test_get_win_rate_no_orders(self) -> None:
        """Test win rate with no closed orders."""
        bot = TradingBot(initial_balance=10000.0)
        with pytest.raises(ValueError):
            bot.get_win_rate()

    def test_get_profit_factor(self) -> None:
        """Test profit factor calculation."""
        bot = TradingBot(initial_balance=10000.0)
        # +10 trade
        position1 = bot.open_position(
            symbol="EUR/USD",
            order_type=OrderType.BUY,
            quantity=1.0,
            entry_price=100.0,
        )
        bot.close_position(position1.position_id, exit_price=110.0)

        # -5 trade
        position2 = bot.open_position(
            symbol="GBP/USD",
            order_type=OrderType.BUY,
            quantity=1.0,
            entry_price=100.0,
        )
        bot.close_position(position2.position_id, exit_price=95.0)

        profit_factor = bot.get_profit_factor()
        assert profit_factor == pytest.approx(2.0)

    def test_get_account_stats(self) -> None:
        """Test account statistics."""
        bot = TradingBot(initial_balance=10000.0)
        position = bot.open_position(
            symbol="EUR/USD",
            order_type=OrderType.BUY,
            quantity=1.0,
            entry_price=100.0,
        )
        bot.close_position(position.position_id, exit_price=110.0)

        stats = bot.get_account_stats()
        assert stats["initial_balance"] == 10000.0
        assert stats["current_balance"] == pytest.approx(10010.0)
        assert stats["total_profit_loss"] == pytest.approx(10.0)
        assert stats["return_percentage"] == pytest.approx(0.1)
