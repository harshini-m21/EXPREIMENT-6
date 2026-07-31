import random
import sys
import time

# Increase recursion limit for deep recursion in deterministic worst-case scenarios
sys.setrecursionlimit(20000)


def partition(arr, low, high, counter):
    """Lomuto partition scheme tracking total element comparisons."""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        counter["comps"] += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def deterministic_quicksort(arr, low, high, counter):
    """Deterministic Quicksort (Last element as pivot)."""
    if low < high:
        pivot_idx = partition(arr, low, high, counter)
        deterministic_quicksort(arr, low, pivot_idx - 1, counter)
        deterministic_quicksort(arr, pivot_idx + 1, high, counter)


def randomized_quicksort(arr, low, high, counter):
    """Randomized Quicksort (Random element swapped to last)."""
    if low < high:
        rand_idx = random.randint(low, high)
        arr[rand_idx], arr[high] = arr[high], arr[rand_idx]

        pivot_idx = partition(arr, low, high, counter)
        randomized_quicksort(arr, low, pivot_idx - 1, counter)
        randomized_quicksort(arr, pivot_idx + 1, high, counter)


def benchmark(algorithm, data):
    """Measures execution time (ms) and comparison count for a given quicksort implementation."""
    arr_copy = data.copy()
    counter = {"comps": 0}

    start_time = time.perf_counter()
    algorithm(arr_copy, 0, len(arr_copy) - 1, counter)
    end_time = time.perf_counter()

    elapsed_ms = (end_time - start_time) * 1000
    return counter["comps"], elapsed_ms


# --- Benchmark Suite ---
if __name__ == "__main__":
    N = 5000  # Array size chosen to demonstrate worst-case quadratic behavior

    # Generate test input distributions
    random.seed(42)
    random_arr = [random.randint(1, 100000) for _ in range(N)]
    sorted_arr = list(range(1, N + 1))
    reverse_arr = list(range(N, 0, -1))

    # Nearly sorted: 95% sorted, 5% random swaps
    nearly_sorted_arr = list(range(1, N + 1))
    for _ in range(int(N * 0.05)):
        idx1, idx2 = random.randint(0, N - 1), random.randint(0, N - 1)
        nearly_sorted_arr[idx1], nearly_sorted_arr[idx2] = (
            nearly_sorted_arr[idx2],
            nearly_sorted_arr[idx1],
        )

    inputs = {
        "Random": random_arr,
        "Sorted": sorted_arr,
        "Reverse": reverse_arr,
        "Nearly Sorted": nearly_sorted_arr,
    }

    # Header display
    headers = [
        "Input Type",
        "DQS Comps",
        "DQS Time(ms)",
        "RQS Comps",
        "RQS Time(ms)",
    ]
    header_str = (
        f"{headers[0]:<15} {headers[1]:>12} {headers[2]:>14} "
        f"{headers[3]:>12} {headers[4]:>14}"
    )

    print("=" * len(header_str))
    print(" Deterministic Quicksort (DQS) vs. Randomized Quicksort (RQS)")
    print("=" * len(header_str))
    print(header_str)
    print("-" * len(header_str))

    # Run benchmarks across input types
    for label, test_data in inputs.items():
        dqs_comps, dqs_time = benchmark(deterministic_quicksort, test_data)
        rqs_comps, rqs_time = benchmark(randomized_quicksort, test_data)

        print(
            f"{label:<15} {dqs_comps:>12,d} {dqs_time:>14.2f} "
            f"{rqs_comps:>12,d} {rqs_time:>14.2f}"
        )

    print("-" * len(header_str))