import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.tree import DecisionTreeRegressor

class CustomGradientBoosting(BaseEstimator, RegressorMixin):
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.models = []
        self.initial_prediction = None

    def fit(self, X, y):
        self.initial_prediction = np.mean(y)
        current_predictions = np.full(len(y), self.initial_prediction)
        
        for _ in range(self.n_estimators):
            residuals = y - current_predictions

            tree = DecisionTreeRegressor(max_depth=self.max_depth)
            tree.fit(X, residuals)
            
            predictions = tree.predict(X)
            current_predictions += self.learning_rate * predictions
            
            self.models.append(tree)
            
        return self

    def predict(self, X):
        y_pred = np.full(X.shape[0], self.initial_prediction)
        
        for tree in self.models:
            y_pred += self.learning_rate * tree.predict(X)
            
        return y_pred
