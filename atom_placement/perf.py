import time
import statistics
from atom_placement import AtomPlacement
from search import random_walk, max_value, randomized_max_value

INSTANCES = [
    "instances/i01.txt",
    "instances/i02.txt",
    "instances/i03.txt",
    "instances/i04.txt",
    "instances/i05.txt",
    "instances/i06.txt",
    "instances/i07.txt",
    "instances/i08.txt",
    "instances/i09.txt",
    "instances/i10.txt",
]

STRATEGIES = [
    ("random_walk", random_walk, True),
    ("max_value", max_value, False),
    ("randomized_max_value", randomized_max_value, True),
]

REPEATS = 10
LIMIT = 100


def run_strategy(strategy_func, problem, limit):
    start = time.time()
    node = strategy_func(problem, limit)
    elapsed = time.time() - start
    best_value = node.value()
    steps = node.step
    return elapsed, best_value, steps


def main():
    print("| Instance | Strategy | Time (s) | Best Value | Steps | std Value |")
    print("|----------|----------|----------|------------|-------|------------------|")
    results = {s[0]: [] for s in STRATEGIES}
    for instance in INSTANCES:
        problem = AtomPlacement(instance)
        for strat_name, strat_func, is_random in STRATEGIES:
            times, values, steps = [], [], []
            repeats = REPEATS if is_random else 1
            for _ in range(repeats):
                t, v, s = run_strategy(strat_func, problem, LIMIT)
                times.append(t)
                values.append(v)
                steps.append(s)
            avg_time = statistics.mean(times)
            avg_value = statistics.mean(values)
            avg_steps = statistics.mean(steps)
            std_value = statistics.stdev(values) if len(values) > 1 else 0.0
            results[strat_name].append({
                "instance": instance,
                "avg_time": avg_time,
                "avg_value": avg_value,
                "avg_steps": avg_steps,
                "std_value": std_value,
            })
            print(f"| {instance} | {strat_name} | {avg_time:.4f} | {avg_value:.2f} | {avg_steps:.2f} | {std_value:.2f} |")

    print("\n Summary by Strategy ")
    print("\n --------------------")
    best_strategy = None
    best_mean = float('inf')
    for strat_name in results:
        values = [r["avg_value"] for r in results[strat_name]]
        times = [r["avg_time"] for r in results[strat_name]]
        steps = [r["avg_steps"] for r in results[strat_name]]
        mean_value = statistics.mean(values)
        std_value = statistics.stdev(values) if len(values) > 1 else 0.0
        mean_time = statistics.mean(times)
        mean_steps = statistics.mean(steps)
        print(f"Strategy: {strat_name}")
        print(f"  Mean Best Value: {mean_value:.2f} (Stddev: {std_value:.2f})")
        print(f"  Mean Time: {mean_time:.4f} s")
        print(f"  Mean Steps to Best: {mean_steps:.2f}")
        if mean_value > best_mean:
            best_mean = mean_value
            best_strategy = strat_name
    print("\n Best  strategy with minmum mean best value:", best_strategy)
    
if __name__ == "__main__":
    main()