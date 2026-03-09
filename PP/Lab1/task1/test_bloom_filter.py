import unittest
import math
from bloom_filter import BloomFilter
from counting_bloom_filter import CountingBloomFilter
import uuid

class TestBloomFilter(unittest.TestCase):

    def setUp(self):
        self.n = 15000
        self.eps = 0.01
        self.fill_levels = [0.25, 0.50, 0.75, 0.95]
        
        self.bf = CountingBloomFilter(n=self.n, eps=self.eps)
    
    def test_auto_parameters(self):
        self.assertGreater(self.bf.m, 0)
        self.assertGreater(self.bf.k, 0)

        expected_m = int(- (self.n * math.log(self.eps)) / (math.log(2) ** 2))
        self.assertAlmostEqual(self.bf.m, expected_m, delta=10)
    
    def test_add_contains(self):
        test_elem = "123"
        self.assertFalse(self.bf.contains(test_elem))
        self.bf.add(test_elem)
        self.assertTrue(self.bf.contains(test_elem))
    
    def test_remove(self):
        elem = "666"
        self.bf.add(elem)
        self.assertTrue(self.bf.contains(elem))
        self.bf.remove(elem)
        self.assertFalse(self.bf.contains(elem))
        
        for _ in range(5):
            self.bf.add(elem)
        for _ in range(3):
            self.bf.remove(elem)
        self.assertTrue(self.bf.contains(elem))
        for _ in range(2):
            self.bf.remove(elem)
        self.assertFalse(self.bf.contains(elem))
    
    def test_false_positive_rate(self):
        for fill in self.fill_levels:
            added_count = int(self.n * fill)
            
            added_set = set()
            while len(added_set) < added_count:
                added_set.add(uuid.uuid4())
        
            self.bf.clear()
            for elem in added_set:
                self.bf.add(elem)
            
            theoretical = self.bf.false_positive_probability(added_count)
            
            false_positives = 0
            test_elements = []
            while len(test_elements) < added_count:
                cand = added_set.add(uuid.uuid4())
                if cand not in added_set:
                    test_elements.append(cand)
            
            for elem in test_elements:
                if self.bf.contains(elem):
                    false_positives += 1
            
            experimental = false_positives / added_count
            
            self.assertLess(experimental, theoretical)
    
    def test_union_intersection(self):
        bf1 = BloomFilter(m=self.bf.m, k=self.bf.k)
        bf2 = BloomFilter(m=self.bf.m, k=self.bf.k)
        
        set1 = {f"a_{i}" for i in range(100)}
        set2 = {f"b_{i}" for i in range(100)}
        common = {f"common_{i}" for i in range(50)}
        
        for elem in set1 | common:
            bf1.add(elem)
        for elem in set2 | common:
            bf2.add(elem)
        
        union_bf = bf1 + bf2
        for elem in set1 | set2 | common:
            self.assertTrue(union_bf.contains(elem))
        
        intersect_bf = bf1 - bf2
        for elem in common:
            self.assertTrue(intersect_bf.contains(elem))

    def test_union_intersection_count_filter(self):
        bf1 = CountingBloomFilter(m=self.bf.m, k=self.bf.k)
        bf2 = CountingBloomFilter(m=self.bf.m, k=self.bf.k)
        
        set1 = {f"a_{i}" for i in range(100)}
        set2 = {f"b_{i}" for i in range(100)}
        common = {f"common_{i}" for i in range(50)}
        
        for elem in set1 | common:
            bf1.add(elem)
        for elem in set2 | common:
            bf2.add(elem)
        
        union_bf = bf1 + bf2
        for elem in set1 | set2 | common:
            self.assertTrue(union_bf.contains(elem))
        
        intersect_bf = bf1 - bf2
        for elem in common:
            self.assertTrue(intersect_bf.contains(elem))
