from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
   
    def __init__(self):
        self.tickers = ["SPY", "SH"]  # Assuming SH as the inverse ETF for shorting SPY
        self.data_list = []
   
    @property
    def interval(self):
        return "1day"  # Daily data to determine the opening days

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {"SPY": 0, "SH": 0}  # Initialize allocation to 0 for both assets
        
        # Get the day of the week from the last entry
        # Assuming data structure provides a 'date' field
        data_date = data["ohlcv"][-1]["SPY"]["date"]
        log("Data Date: " + data_date)
        
        # Convert string date to date object
        from datetime import datetime
        date_obj = datetime.strptime(data_date, "%Y-%m-%d")
        day_of_week = date_obj.weekday()  # Monday is 0 and Sunday is 6

        # Check if it's Monday (0) morning, if so buy SPY
        if day_of_week == 0:
            allocation_dict["SPY"] = 1  # Go long on SPY
            log("Monday: Going long on SPY")

        # Check if it's Wednesday (2) morning, if so sell SPY holdings and short SPY
        elif day_of_week == 2:
            allocation_dict["SPY"] = 0  # Close long positions
            allocation_dict["SH"] = 1  # Go short on SPY by buying SH
            log("Wednesday: Closing SPY positions and going short by buying SH")

        return TargetAllocation(allocation_dict)