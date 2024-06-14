from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # This strategy focuses only on SPY
        return ["SPY"]

    @property
    def interval(self):
        # Check price every minute
        return "1min"

    def run(self, data):
        log(str(data))
        # Initialize SPY stake to 0
        spy_stake = 0
        # Access the last 20 minutes data for SPY
        if len(data["ohlcv"]) >= 21:
            last_20_prices = [d["SPY"]["close"] for d in data["ohlcv"][-21:-1]]
            current_price = data["ohlcv"][-1]["SPY"]["close"]
            max_price = max(last_20_prices)
            min_price = min(last_20_prices)
            
            # Open long if current price is higher than the max of the last 20 minutes prices
            if current_price > max_price and data['holdings']['SPY'] != 1:
                spy_stake = 1  # 100% allocation into SPY
                log("Opening long position in SPY")
            # Open short if current price is less than the min of the last 20 minutes prices
            elif current_price < min_price and data['holdings']['SPY'] != -1:
                spy_stake = 0  # Indicates a short position; handling of short positions depends on the platform's ability to execute them
                log("Opening short position in SPY")
        else:
            # If there's not enough data, do nothing
            log("Not enough data available to make a decision")
        
        return TargetAllocation({"SPY": spy_stake})