import numpy as np
import math
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class LinearRegression(SimulationStrategy):
    alpha = float(0)
    theta = np.array([0.0, 0.0, 0.0])
    x = np.array([[0.0, 0.0], [0.0, 0.0]])
    y = np.array([0.0, 0.0])
    iterations = 500
    steps = 5
    overshoot = False

    def __init__(self, _theta, _x, _y, _alpha, _iterations=None, _steps=None):
        _x = np.append(np.ones((_x.__len__(), 1)), _x, axis=1)
        if _x.__len__() != _y.__len__():
            raise ValueError('Incompatible matrix size : x y')
        if _x.shape[1] != _theta.__len__():
            raise ValueError('Incompatible matrix size: x theta')
        if type(_alpha) is not float:
            raise ValueError('_alpha should be float')
        self.theta = _theta
        self.x = _x
        self.y = _y
        self.alpha = _alpha
        if _iterations is not None:
            self.iterations = _iterations
        if _steps is not None:
            self.steps = _steps

    def prediction(self):
        return np.matmul(self.x, self.theta)

    def prediction_for_theta(self, theta):
        return np.matmul(self.x, theta)

    def predict(self, _x):
        _x = np.append(np.ones((_x.__len__(), 1)), _x, axis=1)
        return np.matmul(_x, self.theta)

    def cost(self):
        m = self.y.__len__()
        return (np.matmul(np.ones((1, m)), ((self.prediction()-self.y)**2))/(m*2))[0]

    def cost_for_theta(self, theta):
        m = self.y.__len__()
        return (np.matmul(np.ones((1, m)), ((self.prediction_for_theta(theta)-self.y)**2))/(m*2))[0]

    def gradient_decent(self):
        m = self.y.__len__()
        one = np.ones((1, m))*(self.alpha/m)
        off = np.matmul(one, np.multiply(self.x, np.reshape((self.prediction()-self.y), (-1, 1)))).flatten()
        self.theta = self.theta-off

    def feature_normalize(self):
        mean = np.mean(self.x[:, 1:], axis=1).reshape(-1, 1)
        std = np.std(self.x[:, 1:], axis=1).reshape(-1, 1)
        self.x[:, 1:] = (self.x[:, 1:]-mean)/std

    def get_theta(self):
        return self.theta

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def run(self):
        for i in range(self.iterations):
            self.gradient_decent()

    def get_data(self):
        costs = []
        thetas = []
        theta = []
        for i in range(self.iterations):
            if self.cost() > 1000000000000:
                self.iterations = i
                self.steps = math.ceil(i / 10)
                self.overshoot = True
                break
            theta.append(self.theta.tolist())
            costs.append(self.cost())
            self.gradient_decent()
        for i in range(theta.__len__()):
            if i % self.steps == 0:
                thetas.append(theta[i])
        data = dict()
        data['x'] = self.get_x()[:, 1:].flatten().tolist()
        data['y'] = self.get_y().tolist()
        data['costs'] = costs
        data['thetas'] = thetas
        data['iterations'] = self.iterations
        data['steps'] = self.steps
        data['alpha'] = self.alpha
        data['overshoot'] = self.overshoot
        return data

