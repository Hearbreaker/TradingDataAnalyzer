from Simulation.calculation_status import CalculationStatus
from Simulation.exponential_moving_average import ExponentialMovingAverage

__author__ = 'raymond'


class Mcad:
	ema15_constant = 15
	ema40_constant = 40

	def __init__(self):
		self.ema15 = ExponentialMovingAverage(Mcad.ema15_constant)
		self.ema40 = ExponentialMovingAverage(Mcad.ema40_constant)

	def evaluate(self, current_price):
		ema15_result = self.ema15.evaluate(current_price)
		ema40_result = self.ema40.evaluate(current_price)

		if ema15_result == CalculationStatus.Invalid or ema40_result == CalculationStatus.Invalid:
			return CalculationStatus.Invalid

		return ema15_result - ema40_result

	def reset(self):
		self.ema15.reset()
		self.ema40.reset()
