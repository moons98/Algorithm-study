# -*- coding: utf-8 -*-
import sys

"""
연산이 1억번, 1000 -> N^2으로 풀어도 된다
DP problem
"""

N = int(sys.stdin.readline())
num = list(map(int, sys.stdin.readline().split()))

dp = [1 for _ in range(N)]

for i in range(N):
    for j in range(i):
        if num[j] > num[i]:
            dp[i] = max(dp[j] + 1, dp[i])

print(max(dp))
