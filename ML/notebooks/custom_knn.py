import numpy as np
from collections import Counter

class CustomKNN:
    def __init__(self, k=3, metric='euclidean'):
        self.k = k
        self.metric = metric
        self.X_train = None
        self.y_train = None
        self.classes_ = None
        
    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)
        self.classes_ = np.unique(y)
        return self
    
    def _compute_distances_optimized(self, X):
        X = np.array(X)
        n_test = X.shape[0]
        n_train = self.X_train.shape[0]
        distances = np.empty((n_test, n_train))

        if self.metric == 'euclidean':
            X_sq = np.sum(X**2, axis=1).reshape(-1, 1)
            X_train_sq = np.sum(self.X_train**2, axis=1).reshape(1, -1)
            distances = np.sqrt(np.maximum(X_sq + X_train_sq - 2 * X @ self.X_train.T, 0))
            
        elif self.metric == 'manhattan':
            for i in range(n_test):
                distances[i, :] = np.sum(np.abs(self.X_train - X[i]), axis=1)
                
        elif self.metric == 'chebyshev':
            for i in range(n_test):
                distances[i, :] = np.max(np.abs(self.X_train - X[i]), axis=1)
        else:
            raise ValueError(f"Unknown metric: {self.metric}")
            
        return distances

    def predict(self, X):
        X = np.array(X)
        distances = self._compute_distances_optimized(X)
        
        k_indices = np.argpartition(distances, self.k, axis=1)[:, :self.k]
        
        predictions = []
        for row_indices in k_indices:
            neighbor_labels = self.y_train[row_indices]
            most_common = Counter(neighbor_labels).most_common(1)[0][0]
            predictions.append(most_common)
            
        return np.array(predictions)
    
    def predict_proba(self, X):
        X = np.array(X)
        distances = self._compute_distances_optimized(X)
        k_indices = np.argpartition(distances, self.k, axis=1)[:, :self.k]
        
        neighbor_labels = self.y_train[k_indices]
        proba = np.zeros((len(X), len(self.classes_)))
        
        for i, cls in enumerate(self.classes_):
            proba[:, i] = np.sum(neighbor_labels == cls, axis=1) / self.k
            
        return proba
