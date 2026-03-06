import unittest
import numpy as np
from hll import HyperLogLog
from Lab1.task2.random_date_generator import random_date_generator
import matplotlib.pyplot as plt

class TestHyperLogLog(unittest.TestCase):
    def generate_stream(self, size):
        gen = random_date_generator()
        return [next(gen) for _ in range(size)]
    
    def test_accuracy(self):
        sizes = {'small': 21000, 'norm': 241000, 'big': 1000111}
        for label, size in sizes.items():
            stream = self.generate_stream(size)
            hll = HyperLogLog(eps=0.001)
            for item in stream:
                hll.add(item)
            true_count = len(set(stream))
            estimate = hll.count()
            error = abs(estimate - true_count)
            error_pct = error / true_count * 100
            print(f"{label}: True={true_count}, Estimate={estimate}, Abs Error={error}, Error%={error_pct:.2f}")

    def test_merge_accuracy(self):
        stream1 = self.generate_stream(21000)
        stream2 = self.generate_stream(241000)

        hll_small = HyperLogLog(eps=0.001)
        for item in stream1:
            hll_small.add(item)

        true_count1 = len(set(stream1))
        estimate1 = hll_small.count()

        error1 = abs(estimate1 - true_count1)
        error_pct1 = error1 / true_count1 * 100

        hll_norm = HyperLogLog(eps=0.001)
        for item in stream2:
            hll_norm.add(item)

        true_count2 = len(set(stream2))
        estimate2 = hll_norm.count()

        error2 = abs(estimate2 - true_count2)
        error_pct2 = error2 / true_count2 * 100

        merged = hll_small + hll_norm
        true_count = len(set(stream1 + stream2))
        estimate = merged.count()

        error = abs(estimate - true_count)
        error_pct = error / true_count * 100
        print(f"\nSmall error={error_pct1:.2f}, Norm error={error_pct2:.2f}")
        print(f"Merged: True={true_count}, Estimate={estimate}, Abs Error={error}, Error%={error_pct:.2f}")

if __name__ == "__main__":
    unittest.main()
