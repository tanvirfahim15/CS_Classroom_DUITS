import numpy as np


class Statistics:
    n = 0
    number_of_items = 0
    given_array = []
    unique_array = []
    mark_array = {}
    frequency_array = []
    mean = 0
    median = 0
    mode = 0
    sum1 = 0
    sum2 = 0
    sum3 = 0
    arr = []
    arr2 = []
    arr3 = []
    count_arr = []
    std_dev = 0
    upper_quartile = 0
    upper_quartile = 0
    decision = [0, 0, 0]



    def __init__(self, _n, _given_array):
        self.n = _n
        self.given_array = _given_array
        for i in range(len(_given_array)):
            self.mark_array[_given_array[i]] = 0;

        self.arr3 = []
        self.arr2 = []
        self.arr = []
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.frequency_array = []
        self.count_arr = []
        self.unique_array = []
        self.sum1 = 0
        self.sum2 = 0
        self.sum3 = 0
        self.decision = [0, 0, 0]

    def solve_function(self, n, given_array):
        for i in range(n):
            self.arr.append(given_array[i])

        for i in range(len(self.arr)):
            if self.mark_array[self.arr[i]] == 0:
                self.mark_array[self.arr[i]] = 1;
                self.unique_array.append(self.arr[i])
            else:
                self.mark_array[self.arr[i]] = self.mark_array[self.arr[i]] + 1

        self.arr.sort()

        self.mean = np.mean(self.arr)
        self.median = np.median(self.arr)
        self.std_dev = np.std(self.arr)

        for i in range(len(self.arr)):
            self.arr2.append(self.arr[i] - self.mean)

        for i in range(len(self.arr)):
            self.arr3.append(self.arr2[i]*self.arr2[i])

        for i in range(len(self.arr)):
            self.sum1 += self.arr[i]
            self.sum2 += self.arr2[i]
            self.sum3 += self.arr3[i]

        self.upper_quartile = np.percentile(self.arr, 75)
        self.lower_quartile = np.percentile(self.arr, 25)
        if self.upper_quartile - self.median == self.median - self.lower_quartile:
            self.decision[1] = 1
        elif self.upper_quartile - self.median < self.median - self.lower_quartile:
            self.decision[0] = 1
        else:
            self.decision[2] = 1;

    def get_data(self):
        self.solve_function(self.n, self.given_array)
        return [self.arr, len(self.arr), self.arr2, self.arr3, self.mean, self.median, self.sum1, self.sum2, self.sum3, self.std_dev, self.lower_quartile, self.upper_quartile, self.upper_quartile-self.lower_quartile, self.decision]