from Simulation.calculation_status import CalculationStatus
from Simulation.sign_function import SignFunction
from Simulation.mcad import Mcad
from Simulation.signal_line import SignalLine
from Simulation.market_snapshot import MarketSnapshot
from Simulation.stock_snapshot_helper import StockSnapshotHelper
from Simulation.visualization_data import VisualizationData

__author__ = 'Albert'


class McadSignalLineCrossoverStrategy:
	def __init__(self, total_capital, num_stocks):
		self.transaction_amount = total_capital / num_stocks
		self.mcads = []
		self.signal_lines = []
		self.old_dels = []
		self.visualization_data = VisualizationData()

		for count in range(num_stocks):
			self.mcads.append(Mcad())

		for count in range(num_stocks):
			self.signal_lines.append(SignalLine())

		for count in range(num_stocks):
			self.old_dels.append(CalculationStatus.Invalid)

	def notify(self, market_snapshot: MarketSnapshot):
		decisions = []

		for i, stock_snapshot in enumerate(market_snapshot.stock_snapshots):
			stock_snapshot_helper = StockSnapshotHelper(stock_snapshot)

			mid_price = stock_snapshot_helper.get_mid_price()
			curr_mcad = self.mcads[i].evaluate(mid_price)
			self.visualization_data.add_price(stock_snapshot.ticker, mid_price)

			if curr_mcad == CalculationStatus.Invalid:
				self.visualization_data.add_mcad(stock_snapshot.ticker, 0)
				self.visualization_data.add_signal_line(stock_snapshot.ticker, 0)
				continue
			else:
				self.visualization_data.add_mcad(stock_snapshot.ticker, curr_mcad)

			signal_line_value = self.signal_lines[i].evaluate(curr_mcad)
			if signal_line_value == CalculationStatus.Invalid:
				self.visualization_data.add_signal_line(stock_snapshot.ticker, 0)
				continue
			else:
				self.visualization_data.add_signal_line(stock_snapshot.ticker, signal_line_value)

			curr_del = SignFunction.evaluate(curr_mcad - signal_line_value)

			if self.old_dels[i] == CalculationStatus.Invalid:
				self.old_dels[i] = curr_del
				continue

			should_buy = SignFunction.evaluate(curr_del) - SignFunction.evaluate(self.old_dels[i])
			self.old_dels[i] = curr_del

			if should_buy > 0:
				decisions.append((stock_snapshot.ticker, -self.transaction_amount))
			elif should_buy < 0:
				decisions.append((stock_snapshot.ticker, +self.transaction_amount))

		return decisions

	def reset(self):
		for mcad in self.mcads:
			mcad.reset()

		for signal_line in self.signal_lines:
			signal_line.reset()

		self.old_dels = [CalculationStatus.Invalid for old_del in self.old_dels]

		visualization_data_holder = self.visualization_data
		self.visualization_data = VisualizationData()

		return visualization_data_holder
