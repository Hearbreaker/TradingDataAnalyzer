from Simulation.calculation_status import CalculationStatus
from Simulation.sign_function import SignFunction
from Simulation.mcad import Mcad
from Simulation.market_snapshot import MarketSnapshot
from Simulation.stock_snapshot import StockSnapshot
from Simulation.stock_snapshot_helper import StockSnapshotHelper
from Simulation.visualization_data import VisualizationData

__author__ = 'raymond'


class VanillaMcadStrategy:
	def __init__(self, total_capital, num_stocks):
		self.transaction_amount = total_capital / num_stocks
		self.mcads = []
		self.old_mcads = []
		self.visualization_data = VisualizationData()

		for count in range(num_stocks):
			self.mcads.append(Mcad())

		for count in range(num_stocks):
			self.old_mcads.append(CalculationStatus.Invalid)

	def notify(self, market_snapshot: MarketSnapshot):
		decisions = []

		for i, stock_snapshot in enumerate(market_snapshot.stock_snapshots):
			stock_snapshot_helper = StockSnapshotHelper(stock_snapshot)

			mid_price = stock_snapshot_helper.get_mid_price()
			curr_mcad = self.mcads[i].evaluate(mid_price)
			self.visualization_data.add_price(stock_snapshot.ticker, mid_price)

			if curr_mcad == CalculationStatus.Invalid:
				self.visualization_data.add_mcad(stock_snapshot.ticker, 0)
				continue
			else:
				self.visualization_data.add_mcad(stock_snapshot.ticker, curr_mcad)

			if self.old_mcads[i] == CalculationStatus.Invalid:
				self.old_mcads[i] = curr_mcad
				continue

			del_mcad = SignFunction.evaluate(curr_mcad) - SignFunction.evaluate(self.old_mcads[i])
			self.old_mcads[i] = curr_mcad

			if del_mcad > 0:
				decisions.append((stock_snapshot.ticker, self.transaction_amount))
			elif del_mcad < 0:
				decisions.append((stock_snapshot.ticker, -self.transaction_amount))

		return decisions

	def reset(self):
		map(lambda mcad: mcad.reset(), self.mcads)
		map(lambda old_mcad: CalculationStatus.Invalid, self.mcads)

		visualization_data_holder = self.visualization_data
		self.visualization_data = VisualizationData()

		return visualization_data_holder
