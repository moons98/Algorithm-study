# -*- coding: utf-8 -*-
import sys

N, K = map(int, sys.stdin.readline().split())

obj = [[0, 0]]
for _ in range(N):
    W, V = map(int, sys.stdin.readline().split())
    obj.append([W, V])

obj.sort()

dp = [[0 for i in range(K + 1)] for j in range(N + 1)]
for n in range(N + 1):
    w, v = obj[n]
    for k in range(K + 1):
        if k == 0 or n == 0:
            dp[n][k] = 0
        elif w <= k:  # 현재 물건의 무게가 들어갈 수 있는 배낭 한계보다 작으면
            dp[n][k] = max(v + dp[n - 1][k - w], dp[n - 1][k])
        else:  # 물건을 더 채우지 못하므로 이전의 값 가져옴
            dp[n][k] = dp[n - 1][k]

print(dp[-1][-1])

"""
DP: https://gsmesie692.tistory.com/m/113
"""
