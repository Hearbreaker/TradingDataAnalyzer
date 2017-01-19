import os
import matplotlib.pyplot as plt
import numpy as np
from Simulation.visualization_data import VisualizationData

__author__ = 'raymond'


class SimulationVisualizer:
	@staticmethod
	def save_visualization_data(date, visualization_data : VisualizationData):
		for ticker, info in visualization_data.info_by_ticker.items():
			SimulationVisualizer._save_plot(ticker, date, info['prices'], info['mcad_history'], info['signal_values'])

	@staticmethod
	def _save_plot(ticker_symbol, date, stock_prices, mcad_history, signal_values):
		minutes_elapsed = np.arange(len(stock_prices))

		figure, (ax1, ax2) = plt.subplots(2, sharex=True)

		#plt.title(ticker_symbol + '--' + str(date))
		ax1.plot(minutes_elapsed, stock_prices, 'b', label='prices')
		ax2.plot(minutes_elapsed, mcad_history, 'r', label='mcad history')
		ax2.plot(minutes_elapsed, signal_values, 'k', label='signal_values')

		'''
		plt.xlabel('minutes elapsed')
		plt.ylabel('price')
		plt.legend(loc='best', shadow=True)
		'''

		sample_file_name = "".join([c for c in ticker_symbol if c.isalpha() or c.isdigit() or c==' ']).rstrip()
		script_dir = os.path.dirname(__file__)
		results_dir = os.path.join(script_dir, 'Results')
		results_dir = os.path.join(results_dir, str(date))
		results_path = os.path.join(results_dir, sample_file_name)

		if not os.path.isdir(results_dir):
			os.makedirs(results_dir)
		figure.savefig(results_path)
		plt.close(figure)

	@staticmethod
	def plot_pnl(Plist):
		plt.plot(Plist, label="PnL")
		plt.xlabel('days')
		plt.ylabel('PnL')
		sample_file_name = "PnL"  # .join([c for c in ticker_symbol if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
		script_dir = os.path.dirname(__file__)
		results_dir = os.path.join(script_dir, 'Results')
		results_path = os.path.join(results_dir, sample_file_name)
		if not os.path.isdir(results_dir):
			os.makedirs(results_dir)
		plt.savefig(results_path)
		plt.close()


	@staticmethod
	def plot_per_stock_pnl(MinList, ticker):
		#390
		DayList = []
		i = 0
		day = 1
		for min in MinList:
			if i < 390 :
				DayList.append(min)
				i += 1
			else:
				SimulationVisualizer._perstockpnl_helper(DayList, day, ticker)
				DayList = []
				day += 1
				i = 0


	@staticmethod
	def _perstockpnl_helper(DayList, day, ticker):
		sample_file_name = "".join([c for c in ticker if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
		sample_file_name = sample_file_name + ' day' + str(day)
		plt.plot(DayList, label="PnL".join(sample_file_name))
		plt.xlabel('Time(min)')
		plt.ylabel('PnL(dollar)')
		script_dir = os.path.dirname(__file__)
		results_dir = os.path.join(script_dir, 'Results')
		results_dir = os.path.join(results_dir, 'PerStockPNL')
		results_dir = os.path.join(results_dir, ticker)
		results_path = os.path.join(results_dir, sample_file_name)
		if not os.path.isdir(results_dir):
			os.makedirs(results_dir)
		plt.savefig(results_path)
		plt.close()