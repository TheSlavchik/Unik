import matplotlib.pyplot as plt
import pandas as pd
from counting_bloom_filter import CountingBloomFilter
import uuid

def analyze_dependence():
    n_fixed = 15000
    eps_values = [0.9, 0.7, 0.5, 0.3, 0.1, 0.05]
    
    results = []
    
    for eps in eps_values:
        bf = CountingBloomFilter(n=n_fixed, eps=eps)
        
        for fill in [0.25, 0.5, 0.75, 0.95]:
            added = int(n_fixed * fill)
            theoretical = bf.false_positive_probability(added)
            practical_fp = 0

            added_set = set()
            while len(added_set) < added:
                added_set.add(uuid.uuid4())
        
            bf.clear()
            for elem in added_set:
                bf.add(elem)

            test_set = set()
            while len(test_set) < n_fixed:
                test_set.add(uuid.uuid4())

            for elem in test_set:
                if bf.contains(elem):
                    practical_fp += 1
            practical_fp /= n_fixed

            results.append({
                'n': n_fixed,
                'eps': eps,
                'm': bf.m,
                'k': bf.k,
                'fill': fill,
                'fill_percent': f"{fill*100:.0f}%",
                'theoretical_fp': theoretical,
                'practical_fp': practical_fp
            })
    
    df = pd.DataFrame(results)
    
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    
    for idx, fill in enumerate([0.25, 0.5, 0.75, 0.95]):
        ax = axes[idx // 2, idx % 2]
        subset = df[df['fill'] == fill]
        ax.plot(subset['eps'], subset['theoretical_fp'], 'b-', label='Theoretical', linewidth=2)
        ax.plot(subset['eps'], subset['practical_fp'], 'ro', label='Practical', markersize=5)
        ax.set_xlabel('eps')
        ax.set_ylabel('theoretical fp')
        ax.set_title(f'Fill {fill*100:.0f}%', fontsize=14)
        ax.grid(True)
        ax.set_xlim([max(eps_values), min(eps_values)])
        ax.set_xlim([max(eps_values), min(eps_values)])
        ax.legend()
    
    plt.tight_layout()
    plt.show()
    
    return df

def compare_variants():
    test_cases = [
        (25000, 0.7),
        (130000, 0.15),
        (750000, 0.05)
    ]
    
    results = []
    
    for n, eps in test_cases:
        bf = CountingBloomFilter(n=n, eps=eps)
        print(f"n={n}, eps={eps}")
        print(f"Precalculated parameters: m={bf.m}, k={bf.k}")
        
        for fill in [0.25, 0.5, 0.75, 0.95]:
            added = int(n * fill)
            theoretical = bf.false_positive_probability(added)
            print(f"fill={fill*100:.0f}%: P(fp)={theoretical:.6f}")
            
            results.append({
                'n': n,
                'eps': eps,
                'm': bf.m,
                'k': bf.k,
                'fill': f"{fill*100:.0f}%",
                'P(fp)': theoretical
            })
        
        print('\n')

if __name__ == "__main__":
    analyze_dependence()
    compare_variants()