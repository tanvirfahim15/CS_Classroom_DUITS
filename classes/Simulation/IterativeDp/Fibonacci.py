import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy

class Fibonacci(SimulationStrategy):
    n = 0
    fib_array = [0, 1]

    def __init__(self, _n):
        self.n = _n
        self.fib_array = [0, 1]

    def fibonacci_function(self, n):
        for i in range(2, n):
            self.fib_array.append(self.fib_array[i - 1] + self.fib_array[i - 2])

    def get_data(self):
        self.fibonacci_function(self.n)
        return self.fib_array