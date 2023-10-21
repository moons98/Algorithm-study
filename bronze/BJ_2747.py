# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())

dp = [0, 1] + [0 for _ in range(N - 1)]
for i in range(2, N + 1):
    dp[i] = dp[i - 2] + dp[i - 1]

print(dp[N])
