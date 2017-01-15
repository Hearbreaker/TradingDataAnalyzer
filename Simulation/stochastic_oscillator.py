__author__ = 'Albert'

class StochasticOscillator:
    @staticmethod
    def evaluate(close,lowestlow,highesthigh):
        return (close-lowestlow)/(highesthigh-lowestlow)
