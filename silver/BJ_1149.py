# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
cost = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

for i in range(1, N):
    cost[i][0] += min(cost[i - 1][1:])
    cost[i][1] += min(cost[i - 1][0::2])
    cost[i][2] += min(cost[i - 1][:2])

print(min(cost[-1]))

"""
현재 집에서 각각 색을 칠했을 때, 가장 적은 비용을 사용하는 경우를 합산하면서 저장, DP
"""
