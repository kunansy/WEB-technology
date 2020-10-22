#!/usr/bin/env python3
from math import sqrt
from time import time

squares = []
start = time()
for i in range(10_000_000):
    squares += [sqrt(i**2) + sqrt(i**3)]
print(f"{time() - start:.1f} seconds")
