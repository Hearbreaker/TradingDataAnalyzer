from Models.timestamp_price import TimeStampPrice

__author__ = 'raymond'


class StockSnapshot:
	def __init__(self, ticker: str, ask_price: TimeStampPrice, bid_price: TimeStampPrice):
		self.ticker = ticker
		self.ask_price = ask_price
		self.bid_price = bid_price
