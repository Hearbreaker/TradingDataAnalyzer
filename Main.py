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

	market_history = BloombergDataReader.load_bloomberg_trading_data('Resources/TSX60 Trading Data(BID) Test.csv',
																	 'Resources/TSX60 Trading Data(ASK) Test.csv')
	market = Market(market_history)

	num_of_stocks = market.get_num_stocks()
	initial_capital = capital_per_stock * num_of_stocks

	#Parameter for stochastic oscillator
	look_back_period = 14
	k_percent_period = 3
	d_percent_period = 3
	upper_bound = 0.7
	lower_bound = 0.3

	trader = Trader(McadSignalLineCrossoverStrategy(initial_capital, num_of_stocks), initial_capital, capital_per_stock)
	#trader = Trader(McadZeroCrossoverStrategy(initial_capital, num_of_stocks), initial_capital, capital_per_stock)
	#trader = Trader(StochasticOscillatorStrategy(initial_capital, num_of_stocks, look_back_period, k_percent_period, d_percent_period, upper_bound, lower_bound), initial_capital, capital_per_stock)

	'''
	FOR ALBERT: If you need to run full simulation, please turn off plotting in "trader" by commenting:
			gc.collect()
			SimulationVisualizer.save_visualization_data(market_snapshot_helper.get_date(), visualization_data)
	'''

	market.register(trader)
	market.start()

	evaluator = DailyResultEvaluator(initial_capital)
	print('Calculating daily profit and Loss: ' + format(time.clock(), '.2f') + ' secs')
	Plist = []
	for daily_result in trader.daily_results:
		PnL = evaluator.calculate_profit_and_loss(daily_result)
		print(daily_result.date)
		print(PnL)
		print()
		if PnL < 1000000 :
			Plist.append(PnL)
	sharp_ratio = SharpRatio(trader.daily_results, evaluator).calculate()
	print('Sharp ratio: ', sharp_ratio)
	SimulationVisualizer.plot_pnl(Plist)

	for ticker in trader.per_stock_detail:
		print(ticker)
		SimulationVisualizer.plot_per_stock_pnl(trader.per_stock_detail[ticker], ticker)