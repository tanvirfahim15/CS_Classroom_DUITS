import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class LCS(SimulationStrategy):
    String1 = ""
    String2 = ""
    mat = [0][0]
    parent = [0][0]

    def __init__(self, _string1, _string2):
        self.String1 = _string1
        self.String2 = _string2
        self.mat = [[0 for x in range(len(self.String1) + 1)] for y in range(len(self.String2) + 1)]
        self.parent = [[0 for x in range(len(self.String1) + 1)] for y in range(len(self.String2) + 1)]

    def run(self):
        for i in range(1, len(self.String1) + 1):
            for j in range(1, len(self.String2) + 1):
                if self.String1[i - 1] == self.String2[j - 1]:
                    self.mat[j][i] = self.mat[j - 1][i - 1] + 1
                    self.parent[j][i] = 0
                elif self.mat[j - 1][i] > self.mat[j][i - 1]:
                    self.mat[j][i] = self.mat[j - 1][i]
                    self.parent[j][i] = 1
                else:
                    self.mat[j][i] = self.mat[j][i - 1]
                    self.parent[j][i] = -1

    def get_data(self):
        self.run()
        mark1 = [[[0 for x in range(len(self.String1))] for y in range(len(self.String1))]
                 for z in range(len(self.String2))]
        mark2 = [[[0 for x in range(len(self.String2))] for y in range(len(self.String1))]
                 for z in range(len(self.String2))]

        for i in range(len(self.String1)):
            for j in range(len(self.String2)):
                k = i + 1
                l = j + 1
                while k != 0 and l != 0:
                    if self.parent[l][k] == 0:
                        mark1[j][i][k - 1] = 1
                        mark2[j][i][l - 1] = 1
                        k -= 1
                        l -= 1
                    elif self.parent[l][k] == 1:
                        l -= 1
                    else:
                        k -= 1
        return [mark1, mark2, self.mat, self.parent, self.String1, self.String2]
