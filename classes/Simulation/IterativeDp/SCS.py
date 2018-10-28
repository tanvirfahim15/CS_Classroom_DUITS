import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class SCS(SimulationStrategy):
    String1 = "aaa"
    String2 = "cccd"
    dpArray = [0][0]
    pathArray = [0][0]

    def __init__(self, _string1, _string2):
        self.String1 = _string1
        self.String2 = _string2
        self.dpArray = [[0 for col in range(len(self.String2) + 1)] for row in range(len(self.String1) + 1)]
        self.pathArray = [[0 for x in range(len(self.String2) + 1)] for y in range(len(self.String1) + 1)]

    def solve(self):
        for i in range(0 , len(self.String1) + 1):
            self.dpArray[i][0] = i;
        for i in range(0 , len(self.String2)+1):
            self.dpArray[0][i] = i;
        for i in range(1, len(self.String1) + 1):
            for j in range(1, len(self.String2) + 1):
                if self.String1[i - 1] == self.String2[j - 1]:
                    self.dpArray[i][j] = self.dpArray[i - 1][j - 1] + 1
                    self.pathArray[i][j] = 0
                else:
                    self.dpArray[i][j] = min(self.dpArray[i - 1][j] + 1, self.dpArray[i][j - 1] + 1)
                    self.pathArray[i][j] = 1

    def get_data(self):
        self.solve()
        return [self.dpArray, self.pathArray, self.String1, self.String2]