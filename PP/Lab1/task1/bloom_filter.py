import math
import hashlib
from bitarray import bitarray

class BloomFilter:

    def __init__(self, m=None, k=None, n=None, eps=None):
        if m is not None and k is not None:
            self.m = m
            self.k = k
        elif n is not None and eps is not None:
            self.m = int(- (n * math.log(eps)) / (math.log(2) ** 2))
            self.k = int((self.m / n) * math.log(2))
            if self.k < 1:
                self.k = 1
        else:
            raise ValueError("Values are not specified ('m' and 'k' OR 'n' and 'eps')")
        
        self.array = bitarray(self.m)
        self.array.setall(0)
        self.max_hash = 2 ** 30
    
    def _hash(self, item, seed):
        data = f"{seed}:{item}".encode('utf-8')
        hash_bytes = hashlib.sha256(data).digest()

        hash_int = int.from_bytes(hash_bytes)
        return hash_int % self.max_hash
    
    def _get_indices(self, item):
        indices = []
        for i in range(self.k):
            h = self._hash(item, i)
            indices.append(h % self.m)
        return indices
    
    def add(self, item):
        for idx in self._get_indices(item):
            self.array[idx] = 1
    
    def contains(self, item):
        for idx in self._get_indices(item):
            if self.array[idx] == 0:
                return False
        return True
    
    def clear(self):
        self.array = [0] * self.m
    
    def false_positive_probability(self, n_added):
        return (1 - math.exp(-self.k * n_added / self.m)) ** self.k
    
    def __add__(self, other):
        if self.m != other.m or self.k != other.k:
            raise Exception("Filters must have same 'm' and 'k' for crossing")
        
        result = BloomFilter(m=self.m, k=self.k)
        for i in range(self.m):
            result.array[i] = max(self.array[i], other.array[i])
        return result
    
    def __sub__(self, other):
        if self.m != other.m or self.k != other.k:
            raise Exception("Filters must have same 'm' and 'k' for crossing")
        
        result = BloomFilter(m=self.m, k=self.k)
        for i in range(self.m):
            result.array[i] = min(self.array[i], other.array[i])
        return result