import numpy as np
from sklearn.base import ClassifierMixin, RegressorMixin

class CARTNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class CARTBase:
    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None
        self._criterion_func = None
        self._leaf_value_func = None

    def _build_tree(self, X, y, depth=0):
        n_samples, _ = X.shape
        if n_samples >= self.min_samples_split and (self.max_depth is None or depth < self.max_depth):
            best_feature, best_threshold, best_gain = self._find_best_split(X, y)
            if best_gain > 1e-7:
                left_idx = X[:, best_feature] <= best_threshold
                right_idx = ~left_idx
                left_subtree = self._build_tree(X[left_idx], y[left_idx], depth + 1)
                right_subtree = self._build_tree(X[right_idx], y[right_idx], depth + 1)
                return CARTNode(feature=best_feature, threshold=best_threshold,
                                left=left_subtree, right=right_subtree)
        return CARTNode(value=self._leaf_value_func(y))

    def _find_best_split(self, X, y):
        best_gain = -np.inf
        best_feature, best_threshold = None, None
        parent_val = self._criterion_func(y)
        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature]) 
            for threshold in thresholds:
                left_idx = X[:, feature] <= threshold
                if np.sum(left_idx) == 0 or np.sum(~left_idx) == 0:
                    continue
                left_val = self._criterion_func(y[left_idx])
                right_val = self._criterion_func(y[~left_idx])
                n_left, n_right = np.sum(left_idx), np.sum(~left_idx)
                gain = parent_val - (n_left * left_val + n_right * right_val) / len(y)
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
        return best_feature, best_threshold, best_gain

    def _predict_sample(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_sample(x, node.left)
        return self._predict_sample(x, node.right)

    def fit(self, X, y):
        self.root = self._build_tree(np.array(X), np.array(y))
        return self

    def predict(self, X):
        return np.array([self._predict_sample(x, self.root) for x in np.array(X)])

class CARTClassifier(CARTBase, ClassifierMixin):
    def __init__(self, max_depth=None, min_samples_split=2):
        super().__init__(max_depth, min_samples_split)
        self._criterion_func = self._gini
        self._leaf_value_func = lambda y: np.bincount(y.astype(int)).argmax()

    def _gini(self, y):
        _, counts = np.unique(y, return_counts=True)
        probs = counts / len(y)
        return 1 - np.sum(probs ** 2)

class CARTRegressor(CARTBase, RegressorMixin):
    def __init__(self, max_depth=None, min_samples_split=2):
        super().__init__(max_depth, min_samples_split)
        self._criterion_func = lambda y: np.mean((y - np.mean(y)) ** 2)
        self._leaf_value_func = np.mean
