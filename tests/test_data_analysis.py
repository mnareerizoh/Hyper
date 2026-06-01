"""Tests for hyper.data_analysis module."""

import pytest
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


class TestBasicStatistics:
    """Tests for basic statistical functions."""

    def test_calculate_mean(self) -> None:
        """Test mean calculation."""
        assert calculate_mean([1, 2, 3, 4, 5]) == 3.0
        assert calculate_mean([10]) == 10.0

    def test_calculate_mean_empty_list(self) -> None:
        """Test mean with empty list raises error."""
        with pytest.raises(ValueError):
            calculate_mean([])

    def test_calculate_median(self) -> None:
        """Test median calculation."""
        assert calculate_median([1, 2, 3, 4, 5]) == 3
        assert calculate_median([1, 2, 3, 4]) == 2.5

    def test_calculate_median_empty_list(self) -> None:
        """Test median with empty list raises error."""
        with pytest.raises(ValueError):
            calculate_median([])

    def test_calculate_std_dev(self) -> None:
        """Test standard deviation calculation."""
        result = calculate_std_dev([1, 2, 3, 4, 5])
        assert 1.5 < result < 1.6

    def test_calculate_std_dev_insufficient_values(self) -> None:
        """Test std dev with insufficient values."""
        with pytest.raises(ValueError):
            calculate_std_dev([1])


class TestMovingAverages:
    """Tests for moving average functions."""

    def test_simple_moving_average(self) -> None:
        """Test SMA calculation."""
        result = calculate_simple_moving_average([1, 2, 3, 4, 5], 2)
        assert result == [1.5, 2.5, 3.5, 4.5]

    def test_simple_moving_average_window_larger_than_list(self) -> None:
        """Test SMA with window larger than list."""
        with pytest.raises(ValueError):
            calculate_simple_moving_average([1, 2, 3], 5)

    def test_simple_moving_average_invalid_window(self) -> None:
        """Test SMA with invalid window."""
        with pytest.raises(ValueError):
            calculate_simple_moving_average([1, 2, 3], 0)

    def test_exponential_moving_average(self) -> None:
        """Test EMA calculation."""
        values = [1, 2, 3, 4, 5]
        result = calculate_exponential_moving_average(values, 2)
        assert len(result) == 5
        assert result[0] == 1

    def test_exponential_moving_average_invalid_span(self) -> None:
        """Test EMA with invalid span."""
        with pytest.raises(ValueError):
            calculate_exponential_moving_average([1, 2, 3], 5)


class TestVolatilityAndReturns:
    """Tests for volatility and returns functions."""

    def test_calculate_volatility(self) -> None:
        """Test volatility calculation."""
        prices = [100, 101, 99, 102, 98, 105]
        result = calculate_volatility(prices)
        assert result > 0

    def test_calculate_volatility_insufficient_values(self) -> None:
        """Test volatility with insufficient values."""
        with pytest.raises(ValueError):
            calculate_volatility([100])

    def test_calculate_returns(self) -> None:
        """Test returns calculation."""
        result = calculate_returns([100, 110, 99])
        assert len(result) == 2
        assert result[0] == pytest.approx(10.0)
        assert result[1] == pytest.approx(-10.0)

    def test_calculate_returns_insufficient_values(self) -> None:
        """Test returns with insufficient values."""
        with pytest.raises(ValueError):
            calculate_returns([100])

    def test_calculate_cumulative_returns(self) -> None:
        """Test cumulative returns calculation."""
        result = calculate_cumulative_returns([100, 110, 99])
        assert result[0] == 0.0
        assert result[1] == pytest.approx(10.0)
        assert result[2] == pytest.approx(-1.0)

    def test_calculate_cumulative_returns_empty(self) -> None:
        """Test cumulative returns with empty list."""
        with pytest.raises(ValueError):
            calculate_cumulative_returns([])


class TestRSI:
    """Tests for RSI calculation."""

    def test_calculate_rsi(self) -> None:
        """Test RSI calculation."""
        prices = [44, 44.34, 44.09, 43.61, 44.33, 44.83, 45.10, 45.42, 
                  45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.00, 46.00, 46.00]
        result = calculate_rsi(prices, 14)
        assert len(result) > 0
        assert all(0 <= rsi <= 100 for rsi in result)

    def test_calculate_rsi_invalid_period(self) -> None:
        """Test RSI with invalid period."""
        with pytest.raises(ValueError):
            calculate_rsi([1, 2, 3], 5)


class TestBollingerBands:
    """Tests for Bollinger Bands calculation."""

    def test_calculate_bollinger_bands(self) -> None:
        """Test Bollinger Bands calculation."""
        prices = [20, 21, 22, 21, 20, 19, 20, 21, 22, 23, 22, 21, 
                  20, 19, 20, 21, 22, 23, 24, 25, 26]
        upper, middle, lower = calculate_bollinger_bands(prices, 20, 2)
        
        assert len(upper) == len(middle) == len(lower)
        assert all(l < m < u for l, m, u in zip(lower, middle, upper))

    def test_calculate_bollinger_bands_invalid_period(self) -> None:
        """Test Bollinger Bands with invalid period."""
        with pytest.raises(ValueError):
            calculate_bollinger_bands([1, 2, 3], 5, 2)


class TestSharpeRatio:
    """Tests for Sharpe Ratio calculation."""

    def test_calculate_sharpe_ratio(self) -> None:
        """Test Sharpe Ratio calculation."""
        returns = [1.0, 2.0, -0.5, 1.5, 0.5]
        result = calculate_sharpe_ratio(returns, 2.0, 252)
        assert isinstance(result, float)

    def test_calculate_sharpe_ratio_insufficient_returns(self) -> None:
        """Test Sharpe Ratio with insufficient returns."""
        with pytest.raises(ValueError):
            calculate_sharpe_ratio([1.0])

    def test_calculate_sharpe_ratio_zero_volatility(self) -> None:
        """Test Sharpe Ratio with zero volatility."""
        returns = [1.0, 1.0, 1.0, 1.0]
        result = calculate_sharpe_ratio(returns)
        assert result == 0.0


class TestDrawdown:
    """Tests for maximum drawdown calculation."""

    def test_calculate_max_drawdown(self) -> None:
        """Test maximum drawdown calculation."""
        prices = [100, 120, 110, 90, 95, 105]
        drawdown, start, end = calculate_max_drawdown(prices)
        
        assert drawdown < 0
        assert 0 <= start <= end < len(prices)

    def test_calculate_max_drawdown_only_uptrend(self) -> None:
        """Test max drawdown in uptrend (no drawdown)."""
        prices = [100, 110, 120, 130, 140]
        drawdown, _, _ = calculate_max_drawdown(prices)
        assert drawdown == 0.0

    def test_calculate_max_drawdown_empty_list(self) -> None:
        """Test max drawdown with empty list."""
        with pytest.raises(ValueError):
            calculate_max_drawdown([])


class TestTradeMetrics:
    """Tests for trading metrics."""

    def test_calculate_win_rate(self) -> None:
        """Test win rate calculation."""
        returns = [1.0, -0.5, 2.0, -1.0, 3.0]
        result = calculate_win_rate(returns)
        assert result == 60.0

    def test_calculate_win_rate_all_winning(self) -> None:
        """Test win rate with all winning trades."""
        returns = [1.0, 2.0, 3.0]
        result = calculate_win_rate(returns)
        assert result == 100.0

    def test_calculate_win_rate_all_losing(self) -> None:
        """Test win rate with all losing trades."""
        returns = [-1.0, -2.0, -3.0]
        result = calculate_win_rate(returns)
        assert result == 0.0

    def test_calculate_win_rate_empty(self) -> None:
        """Test win rate with empty list."""
        with pytest.raises(ValueError):
            calculate_win_rate([])

    def test_calculate_profit_factor(self) -> None:
        """Test profit factor calculation."""
        returns = [1.0, -0.5, 2.0, -1.0, 3.0]
        result = calculate_profit_factor(returns)
        assert result == 3.0

    def test_calculate_profit_factor_no_losses(self) -> None:
        """Test profit factor with no losses."""
        returns = [1.0, 2.0, 3.0]
        result = calculate_profit_factor(returns)
        assert result == float("inf")

    def test_calculate_profit_factor_no_profits(self) -> None:
        """Test profit factor with no profits."""
        returns = [-1.0, -2.0, -3.0]
        result = calculate_profit_factor(returns)
        assert result == 0.0
