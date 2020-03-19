import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from pso import ParticleSwarmOptimizedClustering as psoAlgorithm
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.datasets import load_iris


def calc_sse(centroids: np.ndarray, labels: np.ndarray, data_arr: np.ndarray):
    distances = 0
    for i, c in enumerate(centroids):
        idx = np.where(labels == i)
        dist = np.sum((data_arr[idx] - c)**2)
        distances += dist
    return distances


def normalize(x: np.ndarray):

    return (x - x.min(axis=0)) / (x.max(axis=0) - x.min(axis=0))


def quantization_error(centroids: np.ndarray, labels: np.ndarray, data: np.ndarray) -> float:
    error = 0.0
    for i, c in enumerate(centroids):
        idx = np.where(labels == i)
        dist = np.linalg.norm(data[idx] - c)
        dist /= len(idx)
        error += dist
    error /= len(centroids)
    return error


def make_plot(data, kmean_label, pso_label):
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 6))
    ax1.set_title('KMeans')
    ax1.scatter(data[:, 0], data[:, 1], c=kmean_label, cmap='brg')
    ax2.set_title("PSO")
    ax2.scatter(data[:, 0], data[:, 1], c=pso_label, cmap='brg')
    plt.savefig('test.png')
    plt.show()


if __name__ == "__main__":

    file = pd.read_csv('/media/shima/Media/Assignments/2nd_semester/NaturalComputing/Assignment2/Exercise3/seed.txt', sep='\t', header=None)
    #print(file.head())

    data = file.drop([7], axis=1)
    data = data.values
    data = normalize(data)

    """iris = load_iris()
    data = iris.data
    actual_label = list(iris.target_names)"""

    n_cluster = 3

    kmeans = KMeans(n_clusters=n_cluster)
    kmeans.fit(data)
    predicted_kmeans = kmeans.predict(data)

    print('Silhouette:', silhouette_score(data, predicted_kmeans))
    print('SSE:', kmeans.inertia_)
    print('Quantization:', quantization_error(centroids=kmeans.cluster_centers_, data=data, labels=predicted_kmeans))

    pso = psoAlgorithm(n_cluster=n_cluster, n_particles=10, data=data, hybrid=False, max_iter=2000, print_debug=50)
    hist = pso.run()
    predicted_pso = pso.predict(data, pso.gbest_centroids)

    print('Silhouette:', silhouette_score(data, predicted_pso))
    print('SSE:', calc_sse(centroids=pso.gbest_centroids, data_arr=data, labels=predicted_pso))
    print('Quantization:', pso.gbest_score)

    make_plot(data, predicted_kmeans, predicted_pso)


