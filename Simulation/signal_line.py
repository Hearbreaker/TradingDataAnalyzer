from Simulation.calculation_status import CalculationStatus
from Simulation.exponential_moving_average import ExponentialMovingAverage

__author__ = 'raymond'


class SignalLine:
	ema9_constant = 9

	# 9 period EMA of the MCAD
	def __init__(self):
		self.ema9 = ExponentialMovingAverage(SignalLine.ema9_constant)

	def evaluate(self, current_mcad):
		ema9_result = self.ema9.evaluate(current_mcad)

		if ema9_result == CalculationStatus.Invalid:
			return CalculationStatus.Invalid

		return ema9_result

	def reset(self):
		self.ema9.reset()
