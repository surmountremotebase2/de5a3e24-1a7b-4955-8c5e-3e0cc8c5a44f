from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from datetime import datetime

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker symbol for the strategy
        self.ticker = "SPY"

    @property
    def assets(self):
        # Specify which assets the strategy will operate on
        return [self.ticker]

    @property
    def interval(self):
        # Use daily data for checking the date
        return "1day"

    @property
    def data(self):
        # OHLCV data for the asset is required in this strategy
        return [OHLCV(self.ticker)]

    def run(self, data):
        # Initialize allocation dictionary with 0 allocation for SPY
        allocation_dict = {self.ticker: 0}

        # Obtain the latest available date from the data
        latest_date = datetime.fromisoformat(data["ohlcv"][-1][self.ticker]["date"])

        # Check if the latest date is Monday
        if latest_date.weekday() == 0:
            # Buy (or keep) SPY on Monday
            allocation_dict[self.ticker] = 1  # 100% allocation
        # Check if the latest date is Wednesday
        elif latest_date.weekday() == 2:
            # Sell (or keep sold) SPY on Wednesday
            allocation_dict[self.ticker] = 0  # 0% allocation

        # Return the TargetAllocation object with the allocation dictionary
        return TargetAllocation(allocation_dict)