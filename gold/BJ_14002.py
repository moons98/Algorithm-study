# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
num = list(map(int, sys.stdin.readline().split()))

dp = [[1, [str(i)]] for i in num]
for i in range(len(num)):
    for j in range(i):
        if num[i] > num[j] and dp[j][0] + 1 > dp[i][0]:
            dp[i][0] = dp[j][0] + 1
            dp[i][1] = dp[j][1] + [str(num[i])]

dp.sort()
print(dp[-1][0])
print(" ".join(dp[-1][1]))
