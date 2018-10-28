import abc


class SimulationContext:

    def __init__(self, strategy):
        self._strategy = strategy

    def get_data(self):
        return self._strategy.get_data()
