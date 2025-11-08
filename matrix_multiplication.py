#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#  "matplotlib>=3.10.7",
#  "numpy>=2.3.4",
# ]
# ///

from typing import Callable
from multiprocessing import Pool, cpu_count
import timeit
import numpy as np
import matplotlib.pyplot as plt
import argparse

type Matrix = list[list[float]]


def matmul(task: tuple[Matrix, Matrix]) -> Matrix:
    A, B = task
    n, p, m = len(A), len(B), len(B[0])
    C = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

# numpy matrix multiplication
def matmul(task: tuple[Matrix, Matrix]) -> Matrix:
    A, B = task
    A_np = np.array(A)
    B_np = np.array(B)
    result = A_np @ B_np
    return result.tolist()


def sequential_map(
    func: Callable[[tuple[Matrix, Matrix]], Matrix],
    data: list[tuple[Matrix, Matrix]],
) -> None:
    list(map(func, data))


def parallel_map(
    func: Callable[[tuple[Matrix, Matrix]], Matrix],
    data: list[tuple[Matrix, Matrix]],
) -> None:
    with Pool(cpu_count()) as pool:
        pool.map(func, data)


def benchmark(
    func: Callable[[list[tuple[Matrix, Matrix]]], None],
    data: list[tuple[Matrix, Matrix]],
    repeat: int,
) -> list[float]:
    return timeit.repeat(lambda: func(data), repeat=repeat, number=1)


def plot_results(seq_times: list[float], par_times: list[float]) -> None:
    data = [seq_times, par_times]
    labels = ["map", f"pool.map ({cpu_count()} cores)"]
    _fig, ax = plt.subplots()  # type: ignore
    ax.boxplot(data, tick_labels=labels)
    ax.set_ylabel("Seconds (s)")  # type: ignore
    for i, times in enumerate(data, start=1):
        median = np.median(times)
        ax.text(i, median, f"{median:.2f}s", ha="center", va="bottom")  # type: ignore
    plt.show()  # type: ignore


def random_matrix(n: int) -> Matrix:
    return [[float(np.random.rand()) for _ in range(n)] for _ in range(n)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=150, help="matrix size n x n (default: 150)")
    parser.add_argument("--tasks", type=int, default=8, help="number of matrix multiplications (default: 8)")
    parser.add_argument("--repeat", type=int, default=5, help="number of replications (default: 5)")
    parser.add_argument("--plot", action="store_true", help="plot the results")
    args = parser.parse_args()

    data = [(random_matrix(args.size), random_matrix(args.size)) for _ in range(args.tasks)]

    seq_times = benchmark(lambda data: sequential_map(matmul, data), data, repeat=args.repeat)
    par_times = benchmark(lambda data: parallel_map(matmul, data), data, repeat=args.repeat)

    seq_median = np.median(seq_times)
    par_median = np.median(par_times)
    speedup = seq_median / par_median if par_median > 0 else float("inf")

    print(f"Sequential median: {seq_median:.2f}s")
    print(f"Parallel median: {par_median:.2f}s")
    print()
    print(f"Speedup: {speedup:.2f}x")

    if args.plot:
        plot_results(seq_times, par_times)