import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy

class LIS(SimulationStrategy):
    n = 0
    number_of_items = 0
    lis_array = [0][0]
    given_array = []
    mark_array = [0][0]

    def __init__(self, _n, _given_array):
        self.n = _n
        self.given_array = _given_array
        self.lis_array= [[0 for col in range(0 , _n+1)] for row in range(0 , 7)]
        self.mark_array= [[0 for col in range(0 , _n+1)] for row in range(0 , _n+1)]

    def solve_function(self, n, given_array):
        self.lis_array[0][0] = 0
        res = 0;

        for i in range(1, n+1):
            previous_mx = 0;
            previous_id = 0;
            for j in range(0 , i):
                self.mark_array[i][j] = 0
                if given_array[i] > given_array[j]:
                    previous_mx = max(previous_mx , self.lis_array[2][j])
                    self.mark_array[i][j] = 1
                    if(previous_mx==self.lis_array[2][j]):
                        previous_id = j
            self.lis_array[0][i] = i
            self.lis_array[1][i] = given_array[i]
            self.lis_array[2][i] = previous_mx+1
            res = max(res, self.lis_array[2][i])
            self.lis_array[3][i] = given_array[previous_id]
            self.lis_array[4][previous_id] = 1
            for j in range(0, i):
                if(self.lis_array[2][j] + 1 == self.lis_array[2][i] and given_array[i] > given_array[j]):
                    self.lis_array[5][j] = 1
                    break

        for i in range(1, n+1):
            if(self.lis_array[2][i] == res):
                self.lis_array[4][i] = 1
                break

        for i in range(1, n+1):
            if(self.lis_array[2][i] == res):
                self.lis_array[5][i] = 1
                break

    def get_data(self):
        self.solve_function(self.n, self.given_array)
        return [self.lis_array, self.n, self.mark_array]