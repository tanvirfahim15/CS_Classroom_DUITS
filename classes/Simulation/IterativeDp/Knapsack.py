import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy

class KnapSack(SimulationStrategy):
    sack_capacity = 0
    number_of_items = 0
    profits = [0][0]
    items = []
    weights = []

    def __init__(self, _sack_capacity, _number_of_items, _items, _weights):
        self.sack_capacity = _sack_capacity
        self.number_of_items = _number_of_items
        self.profits= [[0 for col in range(0 , _sack_capacity+1)] for row in range(0 , _number_of_items+1)]
        self.items = _items
        self.weights = _weights

    def solve_function(self, sack_capacity, number_of_items, items , weights):
        print(sack_capacity)
        print(number_of_items)
        self.profits[0][0] = 0
        for i in range(0, number_of_items+1):
            for j in range(0 , sack_capacity+1):
                if j - weights[i] >= 0:
                    self.profits[i][j] =max( items[i] + self.profits[i-1][j-weights[i]] , self.profits[i-1][j])
                else:
                    self.profits[i][j] = max(self.profits[i][j] , self.profits[i-1][j])


    def get_data(self):
        self.solve_function(self.sack_capacity, self.number_of_items, self.items , self.weights)
        return [self.profits, self.number_of_items, self.items, self.weights, self.sack_capacity]