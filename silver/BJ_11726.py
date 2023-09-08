# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())

dp = [0, 1, 2, 3] + [0 for _ in range(1000)]
for idx, val in enumerate(dp):
    if idx >= 3:
        dp[idx] = dp[idx - 2] + dp[idx - 1]

print(dp[N] % 10007)

"""
점화식 : x[n] = x[n-1] + x[n-2]

2x1 : (2x1) -> 1

2x2 : (2x1)x2, (1x2)x2 -> 2

2x3 : (2x1)x3, (2x1)x1 + (1x2)x2 -> 3

2x4 : (2x1)x4, (2x1)x2 + (1x2)x2, (1x2)x4 -> 5

2x5 : (2x1)x5, (2x1)x3 + (1x2)x2, (2x1)x1 + (1x2)x4 -> 8
"""
