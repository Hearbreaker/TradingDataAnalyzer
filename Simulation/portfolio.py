from Models.target_exposure import TargetExposure
from Models.portfolio_summary import PortfolioSummary
from Simulation.market_snapshot import MarketSnapshot
from Simulation.market_snapshot_helper import MarketSnapshotHelper

__author__ = 'raymond'


class Portfolio:
	def __init__(self, capital_per_stock):
		self.capital_per_stock = capital_per_stock
		self.shares_by_ticker = {}
		self.target_exposures_by_ticker = {}
		self.cash_by_ticker = {}

	def buy(self, market_snapshot, ticker, amount):
		market_snapshot_helper = MarketSnapshotHelper(market_snapshot)
		num_shares, extra_capital = market_snapshot_helper.convert_capital_to_shares(ticker, amount)
		used_amount = amount - extra_capital
		timestamp = market_snapshot_helper.get_timestamp()
		self._update_capital_exposure(timestamp, ticker, used_amount)

		if self._has_ticker(ticker):
			self.shares_by_ticker[ticker] += num_shares
		else:
			self.shares_by_ticker[ticker] = num_shares
			self.cash_by_ticker[ticker] = self.capital_per_stock

		self.cash_by_ticker[ticker] -= used_amount

		return extra_capital

	def short(self, market_snapshot: MarketSnapshot, ticker, amount):
		market_snapshot_helper = MarketSnapshotHelper(market_snapshot)
		num_shares, extra_capital = market_snapshot_helper.convert_capital_to_shares(ticker, amount)
		used_amount = amount - extra_capital
		timestamp = market_snapshot_helper.get_timestamp()
		self._update_capital_exposure(timestamp, ticker, -used_amount)

		if self._has_ticker(ticker):
			self.shares_by_ticker[ticker] -= num_shares
		else:
			self.shares_by_ticker[ticker] = -num_shares
			self.cash_by_ticker[ticker] = self.capital_per_stock

		self.cash_by_ticker[ticker] += used_amount

		return extra_capital

	def evaluate(self, market_snapshot):
		market_snapshot_helper = MarketSnapshotHelper(market_snapshot)
		profit_by_ticker = {ticker: market_snapshot_helper.convert_shares_to_capital(ticker, share) for ticker, share in self.shares_by_ticker.items()}

		return PortfolioSummary(profit_by_ticker, self.target_exposures_by_ticker)

	def get_snapshot(self, market_snapshot: MarketSnapshot):
		snapshot = {}
		market_snapshot_helper = MarketSnapshotHelper(market_snapshot)

		for ticker in self.shares_by_ticker:
			stock_value = market_snapshot_helper.convert_shares_to_capital(ticker, self.shares_by_ticker[ticker])
			pnl = self.cash_by_ticker[ticker] + stock_value - self.capital_per_stock
			snapshot[ticker] = pnl

		return snapshot

	def clear(self):
		self.shares_by_ticker.clear()
		self.target_exposures_by_ticker = {}
		for ticker in self.cash_by_ticker:
			self.cash_by_ticker[ticker] = self.capital_per_stock

	def _update_capital_exposure(self, timestamp, ticker, used_amount):
		if ticker not in self.target_exposures_by_ticker:
			self.target_exposures_by_ticker[ticker] = []

		self.target_exposures_by_ticker[ticker].append(TargetExposure(timestamp, ticker, used_amount))

	def _has_ticker(self, ticker):
		if ticker in self.shares_by_ticker:
			return True
		else:
			return False

