# -*- coding: utf-8 -*-
import sys
from collections import deque


def dfs(N, K):
    queue = deque([N])
    while queue:
        loc = queue.popleft()
        if loc == K:
            print(trial[loc])
            break
        nx = [loc - 1, loc + 1, loc * 2]
        for i in nx:
            if 0 <= i < 100001 and not trial[i]:
                trial[i] = trial[loc] + 1
                queue.append(i)

    return


N, K = map(int, sys.stdin.readline().split())

trial = [0 for _ in range(100001)]
dfs(N, K)

"""
bfs니까 나중에 갱신되는 값 없이 처음 도달하는 값이 최단거리
"""
