import numpy as np
import math
import random
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class KMeans(SimulationStrategy):
    points = []
    centroids = []
    cluster = []
    max = 0.0
    min = 0.0

    def __init__(self, points, centroids):
        self.points = points
        self.centroids = centroids
        self.cluster = []
        for i in range(len(points)):
            self.cluster.append(0)
        self.max = self.points[0][0]
        self.min = self.points[0][0]
        for point in points:
            for entry in point:
                if self.max < entry:
                    self.max = entry
                if self.min > entry:
                    self.min = entry

    @staticmethod
    def get_distance(p1, p2):
        diff = np.asarray(p1) - np.asarray(p2)
        square_diff = np.matmul(diff, np.transpose(diff))
        return math.sqrt(square_diff)

    def get_cost(self):
        cost = 0.0
        for i in range(len(self.points)):
            cost += KMeans.get_distance(self.points[i],self.centroids[self.cluster[i]])
        return cost/len(self.points)

    def update_cluster(self):
        for i in range(len(self.points)):
            for j in range(len(self.centroids)):
                if KMeans.get_distance(self.points[i], self.centroids[j]) < \
                        KMeans.get_distance(self.points[i], self.centroids[self.cluster[i]]):
                    self.cluster[i] = j
        return

    def update_centroids(self):
        temp_centroid = np.asarray([[0.0 for j in range(len(self.centroids[0]))]for i in range(len(self.centroids))])
        temp_count = [0 for i in range(len(self.centroids))]
        for i in range(len(self.points)):
            temp_count[self.cluster[i]] += 1
            temp_centroid[self.cluster[i]] += self.points[i]
        for i in range(len(temp_centroid)):
            for j in range(len(temp_centroid[i])):
                if temp_count[i] != 0:
                    temp_centroid[i][j] /= temp_count[i]
                else:
                    temp_centroid[i][j] = random.uniform(self.min, self.max)
        self.centroids = temp_centroid.tolist()
        return

    def get_data(self):
        data = dict()
        data['points'] = self.points
        data['clusters'] = list()
        data['centroids'] = list()
        data['costs'] = list()
        latest_centroids=self.centroids
        while True:
            data['clusters'].append(list(self.cluster))
            data['centroids'].append(list(self.centroids))
            data['costs'].append(self.get_cost())
            self.update_cluster()
            data['clusters'].append(list(self.cluster))
            data['centroids'].append(list(self.centroids))
            data['costs'].append(self.get_cost())
            self.update_centroids()
            if self.centroids==latest_centroids:
                break
            latest_centroids=self.centroids
        data['clusters'].append(list(self.cluster))
        data['centroids'].append(list(self.centroids))
        data['costs'].append(self.get_cost())
        return data

