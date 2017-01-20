import gc
from Models.daily_result import DailyResult
from Simulation.portfolio import Portfolio
from Simulation.market_snapshot import MarketSnapshot
from Simulation.market_snapshot_helper import MarketSnapshotHelper
from Simulation.simulation_visualizer import SimulationVisualizer

__author__ = 'raymond'


class Trader:
	def __init__(self, trading_strategy, initial_capital, capital_per_stock, commission):
		self.commission = commission
		self.total_capital_backup = initial_capital
		self.cash = initial_capital
		self.strategy = trading_strategy
		self.portfolio = Portfolio(capital_per_stock)
		self.daily_results = []
		self.per_stock_detail = {}

	def notify(self, market_snapshot: MarketSnapshot):
		market_snapshot_helper = MarketSnapshotHelper(market_snapshot)
		if market_snapshot_helper.is_end_of_trading_hours():
			date = market_snapshot_helper.get_date()
			portfolio_summary = self.portfolio.evaluate(market_snapshot)
			daily_result = DailyResult(date, self.cash, portfolio_summary)
			self.daily_results.append(daily_result)
			self.portfolio.clear()
			visualization_data = self.strategy.reset()
			#visualization_data.add_all_daily_pnl(self.per_stock_detail)
			#gc.collect()  # needed to free up memory for plots
			#SimulationVisualizer.save_visualization_data(market_snapshot_helper.get_date(), visualization_data)
			#self.per_stock_detail.clear()

			self.cash = self.total_capital_backup
			return

		decisions = self.strategy.notify(market_snapshot)

		for ticker, amount in decisions:
			amount -= self.commission
			self.cash -= self.commission

			if amount > 0:
				extra_capital = self.portfolio.buy(market_snapshot, ticker, amount)
				assert extra_capital >= 0
				self.cash -= amount
				self.cash += extra_capital
			elif amount < 0:
				extra_capital = self.portfolio.short(market_snapshot, ticker, abs(amount))
				assert extra_capital >= 0
				self.cash += abs(amount)
				self.cash -= extra_capital
			else:
				print('DEBUG: Should never happen')
				assert False

		'''
		portfolio_snapshot = self.portfolio.get_snapshot(market_snapshot)

		for stock_snapshot in market_snapshot.stock_snapshots:
			ticker = stock_snapshot.ticker

			if ticker not in self.per_stock_detail:
				self.per_stock_detail[ticker] = []

			if ticker in portfolio_snapshot:
				self.per_stock_detail[ticker].append(portfolio_snapshot[ticker])
			else:
				self.per_stock_detail[ticker].append(0)
		'''
