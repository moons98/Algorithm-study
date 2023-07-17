# -*- coding: utf-8 -*-
import sys
from itertools import combinations

N, M = map(int, sys.stdin.readline().split())
S = list(map(int, sys.stdin.readline().split()))

total = set([sum(i) for i in combinations(S, 2)])
S_total = total.union(S)

dp = [0 for _ in range(N + 1)]
dp[0] = -1
for i in S_total:
    if i <= N:
        dp[i] = 1

for idx, val in enumerate(dp):
    if val == 0:
        num_case = [dp[i] + dp[idx - i] for i in range(1, idx // 2 + 1) if dp[i] != -1 and dp[idx - i] != -1]
        if num_case != []:
            dp[idx] = min(num_case)
        else:
            dp[idx] = -1

print(dp[N])
