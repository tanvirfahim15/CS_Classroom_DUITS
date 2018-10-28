import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class CoinChangeVariant3(SimulationStrategy):
    amount = 0
    coin_array_length = 0
    possible = [0][0]
    coin_array = []

    def __init__(self, _n, _k, _coin):
        self.n = _n
        self.coin_array_length = _k
        self.possible= [[0 for x in range(0 , _n+1)] for y in range(0 , _k+1)]
        self.coin_array = _coin

    def solve_function(self, n, k, coin):
        self.possible[0][0] = 1
        for i in range(1, k+1):
            for j in range(0 , n+1):
                if j - coin[i] >= 0:
                    self.possible[i][j] |= self.possible[i-1][j-coin[i]]
                self.possible[i][j] |= self.possible[i-1][j]

    def get_data(self):
        self.solve_function(self.n, self.coin_array_length, self.coin_array)
        return [self.possible , self.coin_array , self.n, self.coin_array_length]