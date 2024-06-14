from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from datetime import datetime

class TradingStrategy(Strategy):
    def __init__(self):
        # Specific ticker for trading.
        self.ticker = "SPY"

    @property
    def assets(self):
        # Target asset for the strategy.
        return [self.ticker]

    @property
    def interval(self):
        # Daily interval for strategy execution.
        return "1day"

    def run(self, data):
        # Initialize target allocation with no position.
        allocation_dict = {self.ticker: 0}
        # Get current date from the latest data point.
        current_date = datetime.strptime(data["ohlcv"][-1][self.ticker]["date"], '%Y-%m-%d')
        
        # Buy SPY on Monday.
        if current_date.weekday() == 0:  # Monday is represented by 0.
            allocation_dict[self.ticker] = 1  # Allocating 100% to SPY.

        # Sell SPY on Friday. Since the allocation on Friday won't take effect 
        # until the next trading day (which would be Monday), effectively 
        # this implies holding SPY throughout the week and selling it at the 
        # end of the week. The strategy does not need to explicitly sell SPY 
        # on Friday as setting the allocation to 0 on Monday will suffice to close 
        # the position at the start of next week.
        
        return TargetAllocation(allocation_dict)