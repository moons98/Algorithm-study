# -*- coding: utf-8 -*-
import sys
from math import inf


def bf(start):
    dist[start] = 0
    for i in range(1, N + 1):
        for cur_node in range(1, N + 1):
            for next_node, time in graph[cur_node]:
                if dist[cur_node] != inf and dist[next_node] > dist[cur_node] + time:
                    dist[next_node] = dist[cur_node] + time
                    if i == N:
                        return True
    return False


N, M = map(int, sys.stdin.readline().split())

graph = [[] for _ in range(N + 1)]
dist = [inf for _ in range(N + 1)]
for i in range(M):
    A, B, C = map(int, sys.stdin.readline().split())
    graph[A].append([B, C])

negative_cycle = bf(1)
if negative_cycle:
    print(-1)
else:
    for i in dist[2:]:
        if i == inf:
            print(-1)
        else:
            print(i)
