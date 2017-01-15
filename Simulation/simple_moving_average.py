import pandas as pd
from Models.queue import Queue
from Simulation.calculation_status import CalculationStatus

__author__ = 'Albert'

class Simple_Moving_Average:

    def __init__(self,first_valid_minute):
        self.first_valid_minute = first_valid_minute
        self.next_minute = 0
        self.price_buffer = Queue(first_valid_minute)

    def evaluate(self, current_data):
        self.next_minute += 1

        if self.next_minute < self.first_valid_minute:
            self.price_buffer.push(current_data)

            return CalculationStatus.Invalid

        else:
            self.price_buffer.push(current_data)

            return self.price_buffer.mean()

    def reset(self):
        self.first_valid_minute = 0
        self.next_minute = 0
        self.price_buffer.clear()


