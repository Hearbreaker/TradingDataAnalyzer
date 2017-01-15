from datetime import datetime, time
from Simulation.stock_snapshot import StockSnapshot

__author__ = 'raymond'


class StockSnapshotHelper:
	def __init__(self, stock_snapshot: StockSnapshot):
		self.stock_snapshot = stock_snapshot
		self._closing_time = time(16, 0, 0)

	def get_mid_price(self):
		return (self.stock_snapshot.ask_price.last_price + self.stock_snapshot.bid_price.last_price) / 2

	def get_high(self):
		return (self.stock_snapshot.ask_price.high_price + self.stock_snapshot.bid_price.high_price) / 2

	def get_low(self):
		return (self.stock_snapshot.ask_price.low_price + self.stock_snapshot.bid_price.low_price) / 2

	def is_end_of_trading_hours(self):
		if self.stock_snapshot.ask_price.datetime.time() == self._closing_time:
			return True
		else:
			return False

	def get_timestamp(self):
		return self.stock_snapshot.ask_price.datetime

	def get_date(self):
		return self.stock_snapshot.ask_price.datetime.date()
