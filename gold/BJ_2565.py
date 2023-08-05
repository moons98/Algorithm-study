# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())

lines = []
for i in range(N):
    x, y = map(int, sys.stdin.readline().split())
    lines.append([x, y])

lines.sort()

# DP, 가장 긴 증가하는 부분수열
dp = [1 for _ in range(N)]
for i in range(N):
    for j in range(i):
        if lines[j][1] < lines[i][1]:
            dp[i] = max(dp[j] + 1, dp[i])

print(N - max(dp))
