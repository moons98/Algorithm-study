# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
dp = [5001 for _ in range(N + 5)]
dp[3], dp[5] = 1, 1

for i in range(6, N + 1):
    dp[i] = min(dp[i - 3], dp[i - 5]) + 1

print(dp[N] if dp[N] < 5001 else -1)
