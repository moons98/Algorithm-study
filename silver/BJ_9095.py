# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())

dp = [0, 1, 2, 4] + [0 for i in range(8)]
for idx, val in enumerate(dp):
    if idx >= 4:
        dp[idx] = dp[idx - 3] + dp[idx - 2] + dp[idx - 1]

answer = []
for _ in range(N):
    num = int(sys.stdin.readline())
    answer.append(dp[num])

for i in answer:
    print(i)


"""
1: 1 -> 1
2: 11, 2 -> 2
3: 111, 12, 21, 3 -> 4

4: 1111, 112, 121, 211, 22, 31, 13 -> 7
5: 11111, 1112, 1121, 1211, 2111, 122, 212, 221, 113, 131, 311, 32, 23 -> 13

DP가 때로는 점화식 찾을 필요가 있다는 것..
"""
