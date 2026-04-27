import time
import statistics
import pandas as pd

def benchmark(impl_name, run_func, pairs, num_runs=50):
    print(f"Benchmarking {impl_name}...")
    times = []
    
    for _ in range(num_runs):
        start = time.perf_counter()
        run_func(pairs)
        end = time.perf_counter()
        elapsed = end - start
        times.append(elapsed)
    
    mean = statistics.mean(times)
    median = statistics.median(times)
    std_dev = statistics.stdev(times)
    min_time = min(times)
    max_time = max(times)
    
    return {
        'min': min_time,
        'max': max_time,
        'mean': mean,
        'median': median,
        'std_dev': std_dev
    }

def run_comparison(functions_to_test, pairs):
    all_results = []
    
    for name, func in functions_to_test.items():
        stats = benchmark(name, func, pairs) 
        all_results.append({
            'Способ': name,
            'Медиана (s)': stats['median'],
            'Среднее (s)': stats['mean'],
            'Min (s)': stats['min'],
            'Std Dev': stats['std_dev']
        })
    
    return pd.DataFrame(all_results)