#!/usr/bin/env python3
import time

import calc


def measure_time(func):
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, *kwargs)
        print(f"{time.time() - start:.1f}")
    return inner


if __name__ == "__main__":
    start = time.time()
    calc.do_math(1, 10_000_000)
    stop = time.time() - start

    print(f"{stop:.1f}")
    print(f"{3.5 / stop:.1f}")
