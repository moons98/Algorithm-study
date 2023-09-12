# -*- coding: utf-8 -*-
import sys
from collections import deque


def bfs(N, K):
    trial = [0 for _ in range(100001)]
    queue = deque([N])
    answer = 0
    while queue:
        loc = queue.popleft()
        if loc == K:
            answer += 1
            if trial[loc] == 0:
                return [trial[K], answer]

        dx = [loc - 1, loc + 1, loc * 2]
        for i in dx:
            if 0 <= i < 100001 and (trial[i] == 0 or trial[i] == trial[loc] + 1):
                trial[i] = trial[loc] + 1
                queue.append(i)

    return [trial[K], answer]


N, K = map(int, sys.stdin.readline().split())
ans = bfs(N, K)
for i in ans:
    print(i)

"""
bfs로 queue에 순서대로 넣으면 최단거리를 찾을 수 있음
최단거리의 수를 찾기 위해서는 최단거리들을 담은 리스트와 중복되는 수 등장하는 변수 필요
"""
