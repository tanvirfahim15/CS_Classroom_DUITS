import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class RodCutting(SimulationStrategy):
    n = 0
    k = 0
    possible = [0][0]
    flag = [0]
    profit = []

    def __init__(self, _n, profit):
        self.n = _n
        self.possible= [[0 for col in range(0 , _k+1)] for row in range(0 , _n+1)]
        self.flag = [0 for x in range(0 , _n+1)]
        self.profit = profit

    def solve_function(self, n, k, coin):
        print(n)
        print(k)
        self.possible[0][0] = 1
        self.flag[0] = 1
        for i in range(0, n+1):
            for j in range(0 , k+1):
                if i - coin[j] >= 0:
                    self.possible[i][j] |= self.flag[i-coin[j]]
                    self.flag[i] |= self.possible[i][j]

    def get_data(self):
        self.solve_function(self.n, self.k, self.coin)
        return [self.possible , self.coin ,self.n , self.k]