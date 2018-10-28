import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class RockClimbing(SimulationStrategy):
    row = 0
    col = 0
    inf = 10**9
    dp_matrix = [0][0]
    cost_matrix = [0][0]

    def __init__(self,  cost):
        self.row = cost.__len__();
        self.col = cost[0].__len__();
        self.dp_matrix= [[0 for col in range(0 , self.col+2)] for row in range(0 , self.row+2)]
        self.cost_matrix = cost

    def solve_function(self, cost):
        for i in range(1 , self.col+1):
            self.dp_matrix[0][1] = int(0)
        for i in range(0 , self.row+2):
            self.dp_matrix[i][0] = int(self.inf)
            self.dp_matrix[i][self.col+1] = int(self.inf)
        for i in range(1, self.row+1):
            for j in range(1 , self.col+1):
                self.dp_matrix[i][j] = min(cost[i-1][j-1] + self.dp_matrix[i-1][j-1] , cost[i-1][j-1] + self.dp_matrix[i-1][j], cost[i-1][j-1] + self.dp_matrix[i-1][j-1])

    def get_data(self):
        print("here")
        for i in range(0 , self.row):
            for j in range(0, self.col):
                print(self.cost_matrix[i][j])

        self.solve_function(self.cost_matrix)
        print("here2")
        for i in range(0, self.row):
            for j in range(0, self.col):
                print(self.dp_matrix[i][j])

        return [self.dp_matrix, self.cost_matrix , self.row , self.col]