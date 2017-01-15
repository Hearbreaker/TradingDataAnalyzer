from Models.timestamp_price import TimeStampPrice
from Simulation.stock_snapshot import StockSnapshot

__author__ = 'raymond'


class StockHistoryRecord:
	def __init__(self, ticker_symbol: str):
		self.ticker_symbol = ticker_symbol
		self.prices_by_type = {'ASK': [], 'BID': []}

	def add_time_stamp_price(self, time_stamp_price: TimeStampPrice, price_type):
		if price_type == 'BID':
			self.prices_by_type['BID'].append(time_stamp_price)
		elif price_type == 'ASK':
			self.prices_by_type['ASK'].append(time_stamp_price)


	def get_next(self):
		for prices in zip(self.prices_by_type['ASK'], self.prices_by_type['BID']):
			yield StockSnapshot(self.ticker_symbol, prices[0], prices[1])
