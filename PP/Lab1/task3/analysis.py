import matplotlib.pyplot as plt
import pandas as pd
from count_min_sketch import CountMinSketch
from collections import Counter
from random_date_generator import generate_stream

def analyze():
    eps_values = [1e-3, 1e-4, 1e-5, 1e-6]
    delta = 0.1
    data = generate_stream(100000)
    true_counts = Counter(data)
    results = []

    for eps in eps_values:
        cms = CountMinSketch(eps=eps, delta=delta)
        for x in data: cms.add(x)
        
        abs_errors = [cms.estimate(x) - true_counts[x] for x in true_counts]
        rel_errors = [(cms.estimate(x) - true_counts[x]) / true_counts[x] for x in true_counts]
        
        results.append({
            'eps': eps,
            'abs_err': sum(abs_errors)/len(abs_errors),
            'rel_err': sum(rel_errors)/len(rel_errors)
        })

    df = pd.DataFrame(results)
    print(df)

    df.plot(x='eps', y=['abs_err', 'rel_err'], marker='o', subplots=True)
    plt.show()
