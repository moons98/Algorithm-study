# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
work = [list(map(int, sys.stdin.readline().split())) for _ in range(N)] + [[1, 0]]

dp = [0 for _ in range(N + 1)]
for i in range(N + 1):
    time, pay = work[i][0], work[i][1]
    dp[i] = max(dp[i - 1], dp[i])
    if i + time < N + 1:
        dp[i + time] = max(dp[i + time], dp[i] + pay)

print(dp[-1])
