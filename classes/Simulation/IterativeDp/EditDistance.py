import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class EditDistance(SimulationStrategy):
    String1 = ""
    String2 = ""
    dp = [0][0]

    def __init__(self, _string1, _string2):
        self.String1 = _string1
        self.String2 = _string2
        self.dp = [[0 for col in range(0 , len(self.String2)+1)] for row in range(0 , len(self.String1)+1)]

    def run(self):
        for i in range(0, len(self.String1)):
            for j in range(0, len(self.String2)):
                if i == 0:
                    self.dp[i][j] = j
                elif j == 0:
                    self.dp[i][j] = i
                elif self.String1[i-1] == self.String2[j-1]:
                    self.dp[i][j] = self.dp[i-1][j-1]
                else:
                    self.dp[i][j] = min(self.dp[i][j-1], min(self.dp[i-1][j], self.dp[i-1][j-1]));



    def get_data(self):
        self.run()

        return [self.dp, self.String1, self.String2]