# -*- coding: utf-8 -*-
import sys


def swap(p1, p2):
    if p1 > x2:
        tmp = p1
        p1 = p2
        p2 = p1

    return p1, p2


N, M = map(int, sys.stdin.readline().split())
map_lst = []
for _ in range(N):
    map_lst.append(list(map(int, sys.stdin.readline().split())))

dp = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
for i in range(1, N + 1):
    for j in range(1, N + 1):
        dp[i][j] = dp[i - 1][j] + dp[i][j - 1] - dp[i - 1][j - 1] + map_lst[i - 1][j - 1]

answer = []
for _ in range(M):
    x1, y1, x2, y2 = map(int, sys.stdin.readline().split())
    if x1 > x2:
        x1, x2 = swap(x1, x2)
    if y1 > y2:
        y1, y2 = swap(y1, y2)

    ans = dp[x2][y2] - dp[x1 - 1][y2] - dp[x2][y1 - 1] + dp[x1 - 1][y1 - 1]
    answer.append(ans)

for i in answer:
    print(i)

"""
단순 for문으로 sum 계산하면 시간초과
prefix-sum, dp로 문제 접근해야 함
-> 한 행씩 처리하려고 하지 말고, 한 번에 2차원 값들을 처리

answer = []
for _ in range(M):
    x1, y1, x2, y2 = map(int, sys.stdin.readline().split())
    if x1 > x2:
        x1, x2 = swap(x1, x2)
    if y1 > y2:
        y1, y2 = swap(y1, y2)

    ans = 0
    for i in range(x1 - 1, x2):
        ans += sum(map_lst[i][y1 - 1 : y2])

    answer.append(ans)
"""
