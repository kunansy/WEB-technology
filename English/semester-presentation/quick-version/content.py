#!/usr/bin/env python3
import time

import calc

if __name__ == "__main__":
    start = time.time()
    calc.do_math(1, 10_000_000)
    stop = time.time() - start

    print(f"{stop:.1f}")
    print(f"{3.5 / stop:.1f}")
