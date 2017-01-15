from Simulation.stochastic_oscillator import StochasticOscillator
from Simulation.calculation_status import CalculationStatus
from Simulation.sign_function import SignFunction
from Simulation.market_snapshot import MarketSnapshot
from Simulation.stock_snapshot_helper import StockSnapshotHelper
from Simulation.simple_moving_average import Simple_Moving_Average
from Simulation.visualization_data import VisualizationData
from Models.queue import Queue


__author__ = 'Albert'

class StochasticOscillatorStrategy:

    def __init__(self,total_capital, num_stocks,look_back_period,k_period,d_period, upper_bound, lower_bound):
        self.transaction_amount = total_capital / num_stocks
        self.high_total_data = []
        self.low_total_data = []
        self.fast_k_percent = []
        self.k_percent = []
        self.old_k_percent = []
        self.d_percent = []
        self.old_d_percent = []
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.visualization_data = VisualizationData()

        for count in range(num_stocks):
            self.high_total_data.append(Queue(look_back_period))
            self.low_total_data.append(Queue(look_back_period))
            self.fast_k_percent.append(Simple_Moving_Average(k_period))
            self.k_percent.append(Simple_Moving_Average(k_period))
            self.old_k_percent.append(CalculationStatus.Invalid)
            self.d_percent.append(Simple_Moving_Average(d_period))
            self.old_d_percent.append(CalculationStatus.Invalid)

    def notify(self, market_snapshot: MarketSnapshot):
        decisions = []

        u_reset = []
        l_reset = []

        for i, stock_snapshot in enumerate(market_snapshot.stock_snapshots):
            u_reset.append(0)
            l_reset.append(0)

            upper = 0
            lower = 0

            stock_snapshot_helper = StockSnapshotHelper(stock_snapshot)

            close_price = stock_snapshot_helper.get_mid_price()
            high = stock_snapshot_helper.get_high()
            low = stock_snapshot_helper.get_low()

            self.high_total_data[i].push(high)
            self.low_total_data[i].push(low)

            highesthigh = self.high_total_data[i].get_max()
            lowestlow = self.low_total_data[i].get_min()

            if self.high_total_data[i].isFull():
                current_fast_k = StochasticOscillator.evaluate(close_price,highesthigh,lowestlow)

                current_k_percent = self.k_percent[i].evaluate(current_fast_k)

                if current_k_percent == CalculationStatus.Invalid:
                    self.old_k_percent[i] = current_k_percent
                    continue
                else:
                    self.old_k_percent[i] = current_k_percent
                    current_d_percent = self.d_percent[i].evaluate(current_k_percent)

                    if current_d_percent == CalculationStatus.Invalid:
                        self.old_d_percent[i] = current_d_percent
                        continue

                    upper = SignFunction.evaluate(current_d_percent - self.upper_bound)

                    lower = SignFunction.evaluate(self.lower_bound - current_d_percent)

                    self.old_d_percent[i] = current_d_percent

            if (upper == 1) and (u_reset[i] == 0):
                dec_value = 1
                u_reset[i] = 1
                l_reset[i] = 0

            elif (lower == 1) and (l_reset[i] == 0):
                dec_value = -1
                u_reset[i] = 0
                l_reset[i] = 1
            else:
                dec_value = 0

            if dec_value > 0:
                decisions.append((stock_snapshot.ticker, +self.transaction_amount))
            elif dec_value < 0:
                decisions.append((stock_snapshot.ticker, -self.transaction_amount))
            else:
                decisions = []


            return decisions


    def reset(self):
        self.high_total_data = []
        self.low_total_data = []
        self.fast_k_percent = []
        self.k_percent = []
        self.old_k_percent = []
        self.d_percent = []
        self.old_d_percent = []

        visualization_data_holder = self.visualization_data
        self.visualization_data = VisualizationData()

        return visualization_data_holder


