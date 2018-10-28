import numpy as np
import sys
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class CoinChangeVariant5(SimulationStrategy):
    amount = 0
    coin_array_length = 0
    needed = [0][0]
    coin_array = []
    path_array = [0][0]
    res = sys.maxsize

    def __init__(self, _n, _k, _coin):
        self.amount = _n
        self.coin_array_length = _k
        self.needed = [[0 for col in range(0, _n + 1)] for row in range(0, _k + 1)]
        self.path_array = [[0 for col in range(0, _n + 1)] for row in range(0, _k + 1)]
        self.coin_array = _coin

    def solve_function(self, n, k, coin):
        for i in range(0, k + 1):
            for j in range(1, n + 1):
                self.needed[i][j] = sys.maxsize

        self.needed[0][0] = 0
        for j in range(1, n + 1):
            self.res = sys.maxsize - 1
            for i in range(1, k + 1):
                if j - coin[i] >= 0:
                    self.res = min(self.needed[i - 1][j - coin[i]], self.needed[i][j - coin[i]])
                self.needed[i][j] = min(self.res + 1, self.needed[i][j])
                if self.needed[i][j] == self.needed[i][j-coin[i]]:
                    self.path_array[i][j] = 1
                else:
                    self.path_array[i][j] = 2
        for i in range(0, k + 1):
            for j in range(0, n + 1):
                if self.needed[i][j] >= sys.maxsize:
                    self.needed[i][j] = -1

    def get_data(self):
        self.solve_function(self.amount, self.coin_array_length, self.coin_array)
        return [self.needed, self.coin_array, self.path_array, self.amount, self.coin_array_length]
