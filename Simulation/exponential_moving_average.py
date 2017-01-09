import pandas as pd
from Simulation.calculation_status import CalculationStatus


class ExponentialMovingAverage:
	def __init__(self, first_valid_minute):
		self.first_valid_minute = first_valid_minute
		self.multiplier = ExponentialMovingAverage._get_multiplier(first_valid_minute)
		self.next_minute = 0
		self.prev_ema = 0
		self.price_buffer = []

	def evaluate(self, current_price):
		self.next_minute += 1

		if self.next_minute < self.first_valid_minute:
			self.price_buffer.append(current_price)

			return CalculationStatus.Invalid
		elif self.next_minute == self.first_valid_minute:
			self.price_buffer.append(current_price)
			price_series = pd.Series(self.price_buffer)
			ema = price_series.mean()
			self.prev_ema = ema

			return ema
		else:
			ema = self.prev_ema + (current_price - self.prev_ema) * self.multiplier
			self.prev_ema = ema

			return ema

	def reset(self):
		self.next_minute = 0
		self.prev_ema = 0
		self.price_buffer.clear()

	@staticmethod
	def _get_multiplier(span):
		return 2 / (span + 1)
