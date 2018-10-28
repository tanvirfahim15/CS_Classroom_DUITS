import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from MachineLearning.LinearRegression import LinearRegression

df = pd.read_csv('data.csv', sep=',', header=None)
arr = np.array(df)
arr = arr.flatten()
x = []
y = []
for i in range(0, arr.size, 2):
    x.append([arr[i]])
    y.append(arr[i + 1])

iterations = 1500
alpha = 0.01
theta = np.array([0.0, 0.0])

x = np.asarray(x)
y = np.asarray(y)


ln = LinearRegression.LinearRegression(theta, x, y, alpha, 2000, 100)
print(ln.get_data())