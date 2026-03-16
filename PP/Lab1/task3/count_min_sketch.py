import math
import mmh3
import numpy as np

class CountMinSketch:
    def __init__(self, d=None, w=None, eps=None, delta=None):
        if eps and delta:
            self.w = int(math.ceil(math.e / eps))
            self.d = int(math.ceil(math.log(1 / delta)))
        else:
            self.d = d
            self.w = w
        self.table = np.zeros((self.d, self.w), dtype=int)

    def add(self, item):
        for i in range(self.d):
            index = mmh3.hash(str(item), i) % self.w
            self.table[i][index] += 1

    def estimate(self, item):
        res = float('inf')
        for i in range(self.d):
            index = mmh3.hash(str(item), i) % self.w
            res = min(res, self.table[i][index])
        return res

    def __add__(self, other):
        new_sketch = CountMinSketch(d=self.d, w=self.w)
        new_sketch.table = self.table + other.table
        return new_sketch
