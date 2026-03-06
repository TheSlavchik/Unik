import unittest
from collections import Counter
from count_min_sketch import CountMinSketch
from random_date_generator import generate_stream

class TestCMS(unittest.TestCase):
    def run_cms_test(self, size, eps=0.0001, delta=0.01):
        data = generate_stream(size)
        true_counts = Counter(data)
        cms = CountMinSketch(eps=eps, delta=delta)
        for x in data: cms.add(x)
        
        errors = [cms.estimate(x) - true_counts[x] for x in true_counts]
        avg_err = sum(errors) / len(errors)
        return cms, avg_err

    def test_implementations(self):
        cms_norm, err_norm = self.run_cms_test(241000)
        cms_big, err_big = self.run_cms_test(1000111)
        print(f"\nNorm Error: {err_norm:.4f}, Big Error: {err_big:.4f}")

    def test_merge(self):
        data1 = generate_stream(1000)
        data2 = generate_stream(1000)
        c1, c2 = Counter(data1), Counter(data2)
        cms1 = CountMinSketch(eps=0.0001, delta=0.01)
        cms2 = CountMinSketch(eps=0.0001, delta=0.01)
        for x in data1: cms1.add(x)
        for x in data2: cms2.add(x)
        
        merged = cms1.merge(cms2)
        combined_true = c1 + c2
        err = sum(merged.estimate(x) - combined_true[x] for x in combined_true) / len(combined_true)
        print(f"Merged Error: {err:.4f}")

if __name__ == "__main__":
    unittest.main()
