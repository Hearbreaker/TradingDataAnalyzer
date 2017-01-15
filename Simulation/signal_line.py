from Simulation.calculation_status import CalculationStatus
from Simulation.exponential_moving_average import ExponentialMovingAverage

__author__ = 'Albert'


class SignalLine:
	ema10_constant = 10

	# 10 period EMA of the MCAD
	def __init__(self):
		self.ema10 = ExponentialMovingAverage(SignalLine.ema10_constant)

	def evaluate(self, current_mcad):
		ema10_result = self.ema10.evaluate(current_mcad)

		if ema10_result == CalculationStatus.Invalid:
			return CalculationStatus.Invalid

		return ema10_result

	def reset(self):
		self.ema10.reset()
