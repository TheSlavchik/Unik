import numpy as np

class KMeansCustom:
    def __init__(self, k=3, max_iters=100, tol=1e-4):
        self.k = k
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None
        self.labels_ = None

    def fit(self, X):
        idx = np.random.choice(len(X), self.k, replace=False)
        self.centroids = X[idx]

        for _ in range(self.max_iters):
            n_samples = X.shape[0]
            distances = np.zeros((n_samples, self.k))

            for i in range(n_samples):
                for j in range(self.k):
                    diff = X[i] - self.centroids[j]
                    distances[i, j] = np.sqrt(np.sum(diff ** 2))

            self.labels_ = np.zeros(n_samples, dtype=int)
            for i in range(n_samples):
                self.labels_[i] = np.argmin(distances[i])

            new_centroids = np.array([
                X[self.labels_ == i].mean(axis=0) if len(X[self.labels_ == i]) > 0 else self.centroids[i] 
                for i in range(self.k)
            ])

            if np.all(np.abs(new_centroids - self.centroids) < self.tol):
                break
            self.centroids = new_centroids
        return self.labels_
