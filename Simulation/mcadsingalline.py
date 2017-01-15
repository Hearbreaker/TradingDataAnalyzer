from Simulation.calculation_status import CalculationStatus
from Simulation.sign_function import SignFunction
from Simulation.mcad import Mcad
from Simulation.market_snapshot import MarketSnapshot
from Simulation.stock_snapshot_helper import StockSnapshotHelper
from Simulation.visualization_data import VisualizationData
from Simulation.exponential_moving_average import ExponentialMovingAverage

__author__ = 'Raymond & Albert'


class McadSignalLine:
    def __init__(self, total_capital, num_stocks):
        self.transaction_amount = total_capital / num_stocks
        self.mcads = []
        self.old_mcads = []
        self.mcad_EMAs = []
        self.old_mcad_EMA = []
        self.visualization_data = VisualizationData()

        for count in range(num_stocks):
            self.mcads.append(Mcad())

        for count in range(num_stocks):
            self.old_mcads.append(CalculationStatus.Invalid)

        for count in range(num_stocks):
            self.mcad_EMAs.append(None)

        for count in range(num_stocks):
            self.old_mcad_EMA.append(CalculationStatus.Invalid)

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
                    self.mcad_EMAs[i] = ExponentialMovingAverage(9)
                    curr_mcad_EMA = self.mcad_EMAs[i].evaluate(curr_mcad)
                else:
                    curr_mcad_EMA = self.mcad_EMAs[i].evaluate(curr_mcad)

            if self.old_mcads[i] == CalculationStatus.Invalid:
                self.old_mcads[i] = curr_mcad
                continue

            if self.old_mcad_EMA[i] == CalculationStatus.Invalid:
                self.old_mcad_EMA[i] = curr_mcad_EMA
                continue

            del_mcad = SignFunction.evaluate(curr_mcad - curr_mcad_EMA) - SignFunction.evaluate(self.old_mcads[i] - self.old_mcad_EMA[i])

            self.old_mcads[i] = curr_mcad
            self.old_mcad_EMA[i] = curr_mcad_EMA

            if del_mcad > 0:
                decisions.append((stock_snapshot.ticker, +self.transaction_amount))
            elif del_mcad < 0:
                decisions.append((stock_snapshot.ticker, -self.transaction_amount))

        return decisions

    def reset(self):
        for mcad in self.mcads:
            mcad.reset()

        for mcad_EMA in self.mcad_EMAs:
            mcad_EMA = None

        self.old_mcads = [CalculationStatus.Invalid for old_mcad in self.old_mcads]
        self.old_mcad_EMA = [CalculationStatus.Invalid for old_mcad in self.old_mcad_EMA]

        visualization_data_holder = self.visualization_data
        self.visualization_data = VisualizationData()

        return visualization_data_holder
