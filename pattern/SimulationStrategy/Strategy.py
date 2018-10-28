import abc


class SimulationStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_data(self):
        pass
