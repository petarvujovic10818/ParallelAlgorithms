import numpy as np
import matplotlib.pyplot as plt
from functools import reduce

data = -2 * np.random.rand(200, 2)

data1 = 1 + 2 * np.random.rand(50, 2)

data2 = 0.5 + np.random.rand(40, 2)
data2[:, 0] = data2[:, 0] - 1

data3 = 0.5 + np.random.rand(40, 2)
data3[:, 0] = (data3[:, 0] - 3)/1.5
data3[:, 1] = data3[:, 1] * 2

data4 = np.random.rand(20, 2)
data4[:, 0] = data4[:, 0] + 2
data4[:, 1] = data4[:, 1] - 1

data[50:100, :] = data1
data[100:140, :] = data2
data[140:180, :] = data3
data[180:200, :] = data4

k = 5
np.random.seed(3)
centroids = np.random.uniform(-2, 3, (k, 2))

def funkcija(data):
    cluster_assignments = np.zeros(data.shape[0], dtype=np.int8)
    for i in range(200):
        distance = np.sqrt(((centroids - data) ** 2).sum(axis=1))
        cluster_assignments[i] = np.argmin(distance)
        return cluster_assignments[i]

def funkcCent(xoo):
    for _ in range(200):
        cluster_assignments = list(map(funkcija, data))
        for i in range(5):
            cluster = [datapoint for j, datapoint in enumerate(data) if cluster_assignments[j] == i]
            centroids[i, 0] = sum(x[0] for x in cluster) / len(cluster)
            centroids[i, 1] = sum(x[1] for x in cluster) / len(cluster)
        return centroids

xx = map(funkcCent, centroids)
print(list(xx))

def show():
    plt.scatter(data[:, 0], data[:, 1])
    cluster_assignments = list(map(funkcija, data))
    for i, c in enumerate(centroids):
        plot = plt.scatter(*c, marker='*', s=150)
        cluster = [datapoint for j, datapoint in enumerate(data) if cluster_assignments[j] == i]
        cluster = np.array(cluster)
        plt.scatter(cluster[:, 0], cluster[:, 1], c=plot.get_facecolor())

    plt.show()

show()