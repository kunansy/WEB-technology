#!/usr/bin/env python3
import math
import time


def do_math(start: int = 0,
            iters_count: int = 0) -> None:
    pos = start
    k_sq = 1_000_000
    while pos < iters_count:
        pos += 1
        math.sqrt((pos - k_sq)**2)


if __name__ == "__main__":
    start = time.time()
    do_math(1, 10_000_000)
    print(f"{time.time() - start:.1f}")
