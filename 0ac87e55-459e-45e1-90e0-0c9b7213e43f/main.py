from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, RSI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define your stocks of interest
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]

    @property
    def assets(self):
        # Assets that the strategy will operate on
        return self.tickers

    @property
    def interval(self):
        # Opting for a daily interval to identify long-term trends
        return "1day"

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Technical indicators for trend and oversold condition check
            long_term_sma = SMA(ticker, data["ohlcv"], length=100)  # Long-term SMA
            short_term_sma = SMA(ticker, data["ohlcv"], length=50)  # Short-term SMA
            rsi_indicator = RSI(ticker, data["ohlcv"], length=14)  # RSI for the oversold condition
            bollinger_bands = BB(ticker, data["ohlcv"], length=20, std=2)  # Bollinger Bands for price level
            
            if not long_term_sma or not short_term_sma or not rsi_indicator or not bollinger_bands:
                log(f"Insufficient data for {ticker}")
                allocation_dict[ticker] = 0
                continue

            current_price = data["ohlcv"][-1][ticker]["close"]
            # Criteria for buying:
            # 1. Long-term downtrend identified by short-term SMA below long-term SMA
            # 2. Current price is near the middle Bollinger Band, acting as a support level
            # 3. Stock is potentially oversold (RSI below 30)
            if (short_term_sma[-1] < long_term_sma[-1] and
                abs(current_price - bollinger_bands["mid"][-1]) / current_price < 0.05 and
                rsi_indicator[-1] < 30):
                log(f"Buying signal for {ticker}")
                allocation_dict[ticker] = 1 / len(self.tickers)  # Equal allocation among satisfying tickers
            else:
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)