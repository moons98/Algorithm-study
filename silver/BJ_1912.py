# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
num = list(map(int, sys.stdin.readline().split()))

dp = [0 for _ in range(N)]
for idx, val in enumerate(num):
    if idx == 0:
        dp[idx] = num[idx]
    else:
        dp[idx] = max(val, dp[idx - 1] + val)

print(max(dp))


"""
자기 자신 or 이전 dp + 자기 자신
"""
