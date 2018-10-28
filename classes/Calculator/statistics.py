import numpy as np


class statistics:
    n = 0
    number_of_items = 0
    given_array = []
    unique_array = []
    mark_array = {}
    frequency_array = []
    mean = 0
    median = 0
    mode = 0
    arr = []
    count_arr = []


    def __init__(self, _n, _given_array):
        self.n = _n
        self.given_array = _given_array
        for i in range(len(_given_array)):
            self.mark_array[_given_array[i]] = 0;

        self.arr = []
        self.mean = 0
        self.median = 0
        self.mode = 0
        self.frequency_array = []
        self.count_arr = []
        self.unique_array = []

    def solve_function(self, n, given_array):
        for i in range(n):
            self.arr.append(given_array[i])

        for i in range(len(self.arr)):
            if self.mark_array[self.arr[i]] == 0:
                self.mark_array[self.arr[i]] = 1;
                self.unique_array.append(self.arr[i])
            else:
                self.mark_array[self.arr[i]] = self.mark_array[self.arr[i]] + 1

        self.unique_array.sort()

        for i in range(len(self.unique_array)):
            self.count_arr.append(self.mark_array[self.unique_array[i]])



        self.mean = np.mean(self.arr)
        self.median = np.median(self.arr)




    def get_data(self):
        self.solve_function(self.n, self.given_array)
        return [self.arr, len(self.unique_array), self.unique_array, self.count_arr , self.mean, self.median]