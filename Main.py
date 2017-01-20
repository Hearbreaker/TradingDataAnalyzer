#!/usr/bin/env python
import time
from BloombergImport.bloomberg_data_reader import BloombergDataReader
from Simulation.market import Market
from Simulation.trader import Trader
from Simulation.mcad_zero_crossover_strategy import McadZeroCrossoverStrategy
from Simulation.mcad_signal_line_crossover_strategy import McadSignalLineCrossoverStrategy
from Simulation.daily_result_evaluator import DailyResultEvaluator
from Simulation.sharp_ratio import SharpRatio
from Simulation.simulation_visualizer import SimulationVisualizer
from Simulation.stochastic_oscillator_strategy import StochasticOscillatorStrategy

__author__ = 'raymond'

if __name__ == '__main__':
	capital_per_stock = 100000

	market_history = BloombergDataReader.load_bloomberg_trading_data('Resources/TSX60 Trading Data(BID).csv',
																	 'Resources/TSX60 Trading Data(ASK).csv')
	market = Market(market_history)

	num_of_stocks = market.get_num_stocks()
	initial_capital = capital_per_stock * num_of_stocks

	#Parameter for stochastic oscillator
	look_back_period = 14
	k_percent_period = 3
	d_percent_period = 3
	upper_bound = 0.7
	lower_bound = 0.3

	trader1 = Trader(McadSignalLineCrossoverStrategy(initial_capital, num_of_stocks), initial_capital, capital_per_stock, 0)
	trader2 = Trader(McadZeroCrossoverStrategy(initial_capital, num_of_stocks), initial_capital, capital_per_stock, 0)
	#trader3 = Trader(StochasticOscillatorStrategy(initial_capital, num_of_stocks, look_back_period, k_percent_period, d_percent_period, upper_bound, lower_bound), initial_capital, capital_per_stock, 6.99)

	'''
	FOR ALBERT: If you need to run full simulation, please turn off plotting in "trader" by commenting:
			gc.collect()
			SimulationVisualizer.save_visualization_data(market_snapshot_helper.get_date(), visualization_data)
	'''

	market.register(trader1)
	market.register(trader2)
	#market.register(trader3)
	market.start()

	evaluator = DailyResultEvaluator(initial_capital)
	print('Calculating daily profit and Loss: ' + format(time.clock(), '.2f') + ' secs')
	sharp_ratio = SharpRatio(trader1.daily_results, evaluator).calculate()
	print('Sharp ratio (signal line): ', sharp_ratio)

	sharp_ratio = SharpRatio(trader2.daily_results, evaluator).calculate()
	print('Sharp ratio (zero line): ', sharp_ratio)

	#sharp_ratio = SharpRatio(trader1.daily_results, evaluator).calculate()
	#print('Sharp ratio (stochastic): ', sharp_ratio)
