# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
num = list(map(int, sys.stdin.readline().split()))

dp = [1 for _ in range(N)]
for i in range(N):
    for j in range(i):
        if num[i] > num[j]:
            dp[i] = max(dp[j] + 1, dp[i])

print(max(dp))

"""
가장 긴 증가하는 부분수열, 시간 제한이 널널해서 N^2으로 해결
"""
