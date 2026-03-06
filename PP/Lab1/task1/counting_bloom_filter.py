from bloom_filter import BloomFilter

class CountingBloomFilter(BloomFilter):
    
    def __init__(self, m=None, k=None, n=None, eps=None):
        super().__init__(m, k, n, eps)
        self.array = [0] * self.m
        self.max_hash = 2 ** 30

    def add(self, item):
        for idx in self._get_indices(item):
            self.array[idx] += 1
    
    def remove(self, item):
        for idx in self._get_indices(item):
            if self.array[idx] > 0:
                self.array[idx] -= 1
    
    def clear(self):
        self.array = [0] * self.m
    
    def get_fill_ratio(self):
        counters_sum = sum(1 for c in self.counters if c > 0)
        return counters_sum / self.m
