"""Trading bot module for Hyper."""

from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum


class OrderType(Enum):
    """Order types for trading."""

    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(Enum):
    """Order status enum."""

    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class TradeSignal(Enum):
    """Trading signals."""

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass
class Order:
    """Represents a trading order."""

    order_id: int
    order_type: OrderType
    symbol: str
    quantity: float
    price: float
    status: OrderStatus
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    profit_loss: Optional[float] = None
    entry_time: Optional[int] = None
    exit_time: Optional[int] = None

    def calculate_profit_loss(self) -> float:
        """
        Calculate profit/loss for the order.

        Returns:
            Profit or loss amount

        Raises:
            ValueError: If entry and exit prices are not set
        """
        if self.entry_price is None or self.exit_price is None:
            raise ValueError("Entry and exit prices required to calculate P&L")

        if self.order_type == OrderType.BUY:
            profit_loss = (self.exit_price - self.entry_price) * self.quantity
        else:
            profit_loss = (self.entry_price - self.exit_price) * self.quantity

        self.profit_loss = profit_loss
        return profit_loss

    def calculate_profit_loss_percentage(self) -> float:
        """
        Calculate profit/loss as percentage.

        Returns:
            Profit/loss percentage

        Raises:
            ValueError: If entry price is not set
        """
        if self.entry_price is None:
            raise ValueError("Entry price required")

        self.calculate_profit_loss()
        if self.profit_loss is None:
            raise ValueError("Cannot calculate percentage without profit/loss")

        percentage = (self.profit_loss / (self.entry_price * self.quantity)) * 100
        return percentage


@dataclass
class Position:
    """Represents an open trading position."""

    position_id: int
    symbol: str
    quantity: float
    entry_price: float
    entry_time: int
    order_type: OrderType
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

    def is_stop_loss_triggered(self, current_price: float) -> bool:
        """
        Check if stop loss is triggered.

        Args:
            current_price: Current market price

        Returns:
            True if stop loss triggered, False otherwise
        """
        if self.stop_loss is None:
            return False

        if self.order_type == OrderType.BUY:
            return current_price <= self.stop_loss
        else:
            return current_price >= self.stop_loss

    def is_take_profit_triggered(self, current_price: float) -> bool:
        """
        Check if take profit is triggered.

        Args:
            current_price: Current market price

        Returns:
            True if take profit triggered, False otherwise
        """
        if self.take_profit is None:
            return False

        if self.order_type == OrderType.BUY:
            return current_price >= self.take_profit
        else:
            return current_price <= self.take_profit

    def calculate_unrealized_pnl(self, current_price: float) -> float:
        """
        Calculate unrealized profit/loss.

        Args:
            current_price: Current market price

        Returns:
            Unrealized P&L amount
        """
        if self.order_type == OrderType.BUY:
            pnl = (current_price - self.entry_price) * self.quantity
        else:
            pnl = (self.entry_price - current_price) * self.quantity

        return pnl

    def calculate_unrealized_pnl_percentage(self, current_price: float) -> float:
        """
        Calculate unrealized profit/loss as percentage.

        Args:
            current_price: Current market price

        Returns:
            Unrealized P&L percentage
        """
        pnl = self.calculate_unrealized_pnl(current_price)
        percentage = (pnl / (self.entry_price * self.quantity)) * 100
        return percentage


class TradingBot:
    """Professional trading bot with risk management."""

    def __init__(
        self,
        initial_balance: float,
        risk_per_trade: float = 1.0,
        max_positions: int = 5,
    ) -> None:
        """
        Initialize the trading bot.

        Args:
            initial_balance: Starting capital in dollars
            risk_per_trade: Risk percentage per trade (1.0 = 1%)
            max_positions: Maximum number of open positions

        Raises:
            ValueError: If initial_balance <= 0 or risk_per_trade <= 0
        """
        if initial_balance <= 0:
            raise ValueError("Initial balance must be positive")
        if risk_per_trade <= 0:
            raise ValueError("Risk per trade must be positive")

        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.risk_per_trade = risk_per_trade
        self.max_positions = max_positions

        self.positions: List[Position] = []
        self.closed_orders: List[Order] = []
        self.order_counter = 0

    def get_position_size(self, stop_loss_distance: float) -> float:
        """
        Calculate position size based on risk per trade.

        Args:
            stop_loss_distance: Distance to stop loss in points/currency

        Returns:
            Position size in units

        Raises:
            ValueError: If stop_loss_distance <= 0
        """
        if stop_loss_distance <= 0:
            raise ValueError("Stop loss distance must be positive")

        risk_amount = self.current_balance * (self.risk_per_trade / 100)
        position_size = risk_amount / stop_loss_distance

        return position_size

    def open_position(
        self,
        symbol: str,
        order_type: OrderType,
        quantity: float,
        entry_price: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        entry_time: int = 0,
    ) -> Position:
        """
        Open a new trading position.

        Args:
            symbol: Trading symbol (e.g., 'EUR/USD')
            order_type: BUY or SELL
            quantity: Position size
            entry_price: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price
            entry_time: Entry timestamp

        Returns:
            The opened position

        Raises:
            ValueError: If max positions reached or invalid parameters
        """
        if len(self.positions) >= self.max_positions:
            raise ValueError(f"Maximum positions ({self.max_positions}) reached")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if entry_price <= 0:
            raise ValueError("Entry price must be positive")

        self.order_counter += 1
        position = Position(
            position_id=self.order_counter,
            symbol=symbol,
            quantity=quantity,
            entry_price=entry_price,
            entry_time=entry_time,
            order_type=order_type,
            stop_loss=stop_loss,
            take_profit=take_profit,
        )

        self.positions.append(position)
        return position

    def close_position(
        self,
        position_id: int,
        exit_price: float,
        exit_time: int = 0,
    ) -> Order:
        """
        Close an open position.

        Args:
            position_id: ID of position to close
            exit_price: Exit price
            exit_time: Exit timestamp

        Returns:
            The completed order

        Raises:
            ValueError: If position not found or invalid exit price
        """
        if exit_price <= 0:
            raise ValueError("Exit price must be positive")

        position = next((p for p in self.positions if p.position_id == position_id), None)

        if position is None:
            raise ValueError(f"Position {position_id} not found")

        self.order_counter += 1
        order = Order(
            order_id=self.order_counter,
            order_type=position.order_type,
            symbol=position.symbol,
            quantity=position.quantity,
            price=exit_price,
            status=OrderStatus.FILLED,
            entry_price=position.entry_price,
            exit_price=exit_price,
            entry_time=position.entry_time,
            exit_time=exit_time,
        )

        # Calculate P&L
        order.calculate_profit_loss()

        # Update balance
        if order.profit_loss is not None:
            self.current_balance += order.profit_loss

        # Close position
        self.positions.remove(position)
        self.closed_orders.append(order)

        return order

    def get_open_positions(self) -> List[Position]:
        """
        Get all open positions.

        Returns:
            List of open positions
        """
        return self.positions.copy()

    def get_closed_orders(self) -> List[Order]:
        """
        Get all closed orders.

        Returns:
            List of closed orders
        """
        return self.closed_orders.copy()

    def get_total_profit_loss(self) -> float:
        """
        Calculate total realized profit/loss.

        Returns:
            Total P&L from closed orders
        """
        total_pnl = sum(
            order.profit_loss or 0 for order in self.closed_orders if order.profit_loss
        )
        return total_pnl

    def get_win_rate(self) -> float:
        """
        Calculate win rate from closed orders.

        Returns:
            Win rate as percentage (0-100)

        Raises:
            ValueError: If no closed orders
        """
        if not self.closed_orders:
            raise ValueError("No closed orders to calculate win rate")

        winning_orders = sum(
            1 for order in self.closed_orders if order.profit_loss and order.profit_loss > 0
        )
        win_rate = (winning_orders / len(self.closed_orders)) * 100

        return win_rate

    def get_profit_factor(self) -> float:
        """
        Calculate profit factor.

        Returns:
            Profit factor (gross profit / gross loss)

        Raises:
            ValueError: If no closed orders
        """
        if not self.closed_orders:
            raise ValueError("No closed orders to calculate profit factor")

        gross_profit = sum(
            order.profit_loss for order in self.closed_orders if order.profit_loss and order.profit_loss > 0
        )
        gross_loss = abs(
            sum(
                order.profit_loss
                for order in self.closed_orders
                if order.profit_loss and order.profit_loss < 0
            )
        )

        if gross_loss == 0:
            return 0.0 if gross_profit == 0 else float("inf")

        return gross_profit / gross_loss

    def get_account_stats(self) -> dict:
        """
        Get comprehensive account statistics.

        Returns:
            Dictionary with account stats
        """
        stats = {
            "initial_balance": self.initial_balance,
            "current_balance": self.current_balance,
            "total_profit_loss": self.get_total_profit_loss(),
            "return_percentage": (
                ((self.current_balance - self.initial_balance) / self.initial_balance) * 100
            ),
            "open_positions": len(self.positions),
            "closed_orders": len(self.closed_orders),
            "win_rate": self.get_win_rate() if self.closed_orders else 0,
            "profit_factor": self.get_profit_factor() if self.closed_orders else 0,
        }
        return stats
