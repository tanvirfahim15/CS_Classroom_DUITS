import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class MatrixChainMultiplication(SimulationStrategy):
    number_of_matrix = 0
    dp_matrix = [0][0]
    dimensions = []

    def __init__(self, number_of_matrix, dimensions):
        self.number_of_matrix = number_of_matrix
        self.dp_matrix= [[0 for col in range(0, number_of_matrix)] for row in range(0, number_of_matrix)]
        self.dimensions = dimensions

    def solve_function(self, number_of_matrix, dimensions):
        self.dp_matrix[0][0] = 0
        for step in range(2, number_of_matrix):
            for i in range(1 , number_of_matrix - step + 1):
                j = step+i-1
                self.dp_matrix[i][j] = 10**20
                for k in range(i , j):
                    self.dp_matrix[i][j] = min(self.dp_matrix[i][j] , self.dp_matrix[i][k] + self.dp_matrix[k + 1][j] + dimensions[i - 1] * dimensions[k] * dimensions[j])

    def get_data(self):
        self.solve_function(self.number_of_matrix, self.dimensions)
        return [self.dp_matrix, self.dimensions , self.number_of_matrix]