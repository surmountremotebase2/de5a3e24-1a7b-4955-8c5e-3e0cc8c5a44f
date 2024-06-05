from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]  # Example tickers, replace with the universe of U.S. stocks.
        self.stop_loss_percentage = 0.02  # 2% trailing stop loss.
        self.stop_loss_prices = {ticker: None for ticker in self.tickers}  # Stop-loss price tracker for each stock.

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"  # Daily data for SMA calculation.

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            ohlcv = data['ohlcv']
            if ticker not in ohlcv:
                continue  # Skip if ticker's data is missing.

            close_prices = [x[ticker]['close'] for x in ohlcv]
            sma20 = SMA(ticker, ohlcv, 20)

            if len(close_prices) < 20 or not sma20:
                continue  # Ensure there's enough data for SMA calculation.
            
            current_price = close_prices[-1]
            current_sma20 = sma20[-1]

            # Check if SMA20 crosses above the price indicating a buy signal.
            if current_sma20 > current_price and (self.stop_loss_prices[ticker] is None or current_price > self.stop_loss_prices[ticker]):
                allocation_dict[ticker] = 1.0 / len(self.tickers)  # Equally divide allocation among tickers.
                # Set a new stop loss price based on the current price.
                self.stop_loss_prices[ticker] = current_price * (1 - self.stop_loss_percentage)
            else:
                allocation_dict[ticker] = 0.0  # No allocation if conditions are not met.

            # Implement trailing stop loss - if current price drops below the stop-loss price, we sell.
            if self.stop_loss_prices[ticker] and current_price < self.stop_loss_prices[ticker]:
                allocation_dict[ticker] = 0.0
                log(f"Triggering stop loss for {ticker} at price {current_price}")

        return TargetAllocation(allocation_dict)