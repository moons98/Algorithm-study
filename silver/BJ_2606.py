# -*- coding: utf-8 -*-
import sys
from collections import deque


def bfs(graph, num):
    visited = [0 for _ in graph]
    queue = deque()
    queue.append(num)
    while queue:
        n = queue.popleft()
        for i in graph[n]:
            if not visited[i]:
                visited[i] += 1
                queue.append(i)

    return max(sum(visited) - 1, 0)


N = int(sys.stdin.readline())
pair = int(sys.stdin.readline())

graph = [[] for _ in range(N + 1)]
for _ in range(pair):
    n, m = map(int, sys.stdin.readline().split())
    graph[n].append(m)
    graph[m].append(n)

print(bfs(graph, 1))

"""
아래 반례에 대해서 처리를 해주지 않으면 -1이 나옴
1
0
"""
