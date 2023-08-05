# -*- coding: utf-8 -*-
import sys


def bf(dist):
    # 처음 업데이트를 시작할 수 있는 노드를 만들어줘야 함
    # 시작 노드가 정해지지 않음
    for i in range(1, N + 1):
        # 모든 노드, 모든 간선 탐색
        for cur_node in range(1, N + 1):
            for next_node, time in graph[cur_node]:
                if dist[cur_node] + time < dist[next_node]:
                    dist[next_node] = dist[cur_node] + time
                    if i == N:
                        return True  # negative cycle
    return False


TC = int(sys.stdin.readline())
lst = []
for _ in range(TC):
    N, M, W = map(int, sys.stdin.readline().split())
    graph = [[] for _ in range(N + 1)]
    dist = [10001 for _ in range(N + 1)]

    # bi_dir
    for _ in range(M):
        S, E, T = list(map(int, sys.stdin.readline().split()))
        graph[S].append([E, T])
        graph[E].append([S, T])

    # uni_dir
    for _ in range(W):
        S, E, T = list(map(int, sys.stdin.readline().split()))
        graph[S].append([E, -T])

    negative_cycle = bf(dist)
    lst.append("YES" if negative_cycle else "NO")

for i in lst:
    print(i)

"""
Bellman-Ford
https://8iggy.tistory.com/153
https://letalearns.tistory.com/78

negative cycle만 찾으면 되니까 처음에 0으로 초기화할 필요 없음
"""
