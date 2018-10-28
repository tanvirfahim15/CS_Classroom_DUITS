import numpy as np
import math
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class LogisticRegression(SimulationStrategy):
    x = np.array([[0.0, 0.0], [0.0, 0.0]])
    y = np.array([0.0, 0.0])

    def __init__(self, x, y,iterations, steps, alpha):
        self.x = np.append(np.ones((x.__len__(), 1)), x, axis=1)
        self.y = y
        self.iterations = iterations
        self.steps =steps
        self.alpha = alpha

    def h(self, theta):
        return self.sigmoid(np.matmul(self.x, theta))

    def prediction(self, theta):
        ret = self.h(theta)
        for i in range(ret.size):
            if ret[i] >= 0.5:
                ret[i] = 1
            else:
                ret[i] = 0
        return ret

    @staticmethod
    def sigmoid(vector):
        ret = []
        vector = vector * -1
        for i in vector:
            try:
                ret.append(math.exp(i))
            except:
                ret.append(float('inf'))
        ret = np.ones(ret.__len__()) + ret
        ret = 1 / ret
        return np.asarray(ret)

    def J(self, theta):
        if 0 in self.h(theta) or 1 in self.h(theta):
            return float('inf')
        return (-np.matmul(np.transpose(self.y), np.log(self.h(theta))) - np.matmul(np.transpose(1-self.y), np.log(1-self.h(theta))))/self.y.size

    def gradient_decent(self, theta, alpha):
        m = self.y.__len__()
        one = np.ones((1, m))*(alpha/m)
        off = np.matmul(one, np.multiply(self.x, np.reshape((self.h(theta)-self.y), (-1, 1)))).flatten()
        return theta-off

    def get_data(self):
        iterations, steps, alpha = self.iterations, self.steps, self.alpha
        data = []
        theta = np.array([0, 0, 0])
        iteration = 0
        cost = self.J(theta)
        for iteration in range(iterations):
            if iteration % steps == 0:
                data.append([iteration, theta[0], theta[1], theta[2], cost])
            theta = self.gradient_decent(theta, alpha)
            cost = self.J(theta)
            if cost == float('inf'):
                break
        data.append([iteration + 1, theta[0], theta[1], theta[2], self.J(theta)])
        return np.asarray(data).flatten().tolist()


