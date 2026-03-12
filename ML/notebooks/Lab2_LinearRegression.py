import numpy as np

class LinearRegressionSGD:
    def __init__(self, lr=0.01, epochs=100, alpha=0.1):
        self.lr = lr
        self.epochs = epochs
        self.alpha = alpha
        self.w = None
        self.b = 0

    def fit(self, X, y):
        X = np.array(X, dtype=np.float64)
        y = np.array(y, dtype=np.float64)
        
        self.mean = X.mean(axis=0)
        self.std = X.std(axis=0)
        self.std[self.std == 0] = 1
        X = (X - self.mean) / self.std
        
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        
        for _ in range(self.epochs):
            indices = np.random.permutation(n_samples)
            for idx in indices:
                xi, yi = X[idx], y[idx]
                prediction = np.dot(xi, self.w) + self.b
                error = prediction - yi
                
                self.w -= self.lr * (error * xi + self.alpha * self.w)
                self.b -= self.lr * error

    def predict(self, X):
        X = np.array(X, dtype=np.float64)
        X = (X - self.mean) / self.std
        return np.dot(X, self.w) + self.b