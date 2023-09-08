# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())

stairs = [0, 0]
for _ in range(N):
    stairs.append(int(sys.stdin.readline()))

dp = [i for i in stairs]
for idx, val in enumerate(stairs):
    if idx < 3:
        continue
    dp[idx] = max(dp[idx] + dp[idx - 2], dp[idx] + stairs[idx - 1] + dp[idx - 3])

print(dp[-1])


"""
7
10
20
25
50
35
10
20

6
40 
40 
20 
1 
20 
5

어렵게 접근하지 말고 두 케이스를 나눠서 직접 i-3 값까지 접근하면 풀림
"""
