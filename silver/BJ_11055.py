# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
num = list(map(int, sys.stdin.readline().split()))

dp = [i for i in num]
for i in range(len(num)):
    for j in range(i):
        if num[i] > num[j] and dp[j] + num[i] > dp[i]:
            dp[i] = dp[j] + num[i]

print(max(dp))


"""
10
1 100 2 50 60 3 5 6 7 8
"""
