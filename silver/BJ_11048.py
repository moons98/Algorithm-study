# -*- coding: utf-8 -*-
import sys

N, M = map(int, sys.stdin.readline().split())
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

dp = [[0 for _ in range(M)] for _ in range(N)]
for x in range(N):
    for y in range(M):
        if 1 <= x and 1 <= y:
            dp[x][y] = max(dp[x][y - 1] + map_lst[x][y], dp[x - 1][y] + map_lst[x][y])
        elif 1 > x:
            dp[x][y] = dp[x][y - 1] + map_lst[x][y]
        elif 1 > y:
            dp[x][y] = dp[x - 1][y] + map_lst[x][y]
        else:
            dp[x][y] = map_lst[x][y]

print(dp[-1][-1])
