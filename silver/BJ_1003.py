# -*- coding: utf-8 -*-
import sys

T = int(sys.stdin.readline())

dp = [[0, 0] for _ in range(41)]
dp[0], dp[1] = [1, 0], [0, 1]

for i in range(2, 41):
    dp[i] = [sum(j) for j in zip(dp[i - 2], dp[i - 1])]

answer = []
for _ in range(T):
    N = int(sys.stdin.readline())
    answer.append(dp[N])

for i in answer:
    print(" ".join(map(str, i)))
