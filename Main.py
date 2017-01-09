#!/usr/bin/env python
import time
from datetime import date
from Models.market_history import MarketHistory
from BloombergImport.bloomberg_data_reader import BloombergDataReader
from Simulation.market import Market
from Simulation.trader import Trader
from Simulation.vanilla_mcad_strategy import VanillaMcadStrategy
from Simulation.simulation_visualizer import SimulationVisualizer
from Simulation.daily_result_evaluator import DailyResultEvaluator
from Simulation.sharp_ratio import SharpRatio


__author__ = 'raymond'

if __name__ == '__main__':
	capital_per_stock = 100000

	market_history = BloombergDataReader.load_bloomberg_trading_data('Resources/TSX60 Trading Data(BID).csv',
																	 'Resources/TSX60 Trading Data(ASK).csv')
	market = Market(market_history)

	num_of_stocks = market.get_num_stocks()
	initial_capital = capital_per_stock * num_of_stocks
	trader = Trader(VanillaMcadStrategy(initial_capital, num_of_stocks), capital_per_stock * num_of_stocks)

	market.register(trader)
	market.start()

	evaluator = DailyResultEvaluator(initial_capital)
	print('Calculating daily profit and Loss: ' + format(time.clock(), '.2f') + ' secs')
	for daily_result in trader.daily_results:
		PnL = evaluator.calculate_profit_and_loss(daily_result)
		print(daily_result.date)
		print(PnL)
		print()

	sharp_ratio = SharpRatio(trader.daily_results, evaluator).calculate()
	print('Sharp ratio: ', sharp_ratio)
