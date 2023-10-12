# -*- coding: utf-8 -*-
import sys
from collections import deque


def bfs(loc, tg_loc):
    # x, y, d
    queue = deque([[loc[0], loc[1], 0]])
    visited = [[0 for _ in range(N)] for _ in range(N)]
    visited[loc[0]][loc[1]] = 1

    tg = []
    while queue:
        x, y, d = queue.popleft()
        if tg and d > tg[-1][-1]:
            return tg
        elif (x, y) in tg_loc:
            tg.append([x, y, d])
            continue

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 > nx or nx >= N or 0 > ny or ny >= N or map_lst[nx][ny] == 1 or visited[nx][ny]:
                continue

            elif d + 1 <= F:
                visited[nx][ny] = 1
                queue.append([nx, ny, d + 1])

    return tg


N, M, F = map(int, sys.stdin.readline().split())

map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
now_loc = tuple(i - 1 for i in map(int, sys.stdin.readline().split()))


passenger = dict()
for i in range(M):
    x1, y1, x2, y2 = list(map(int, sys.stdin.readline().split()))
    passenger[(x1 - 1, y1 - 1)] = (x2 - 1, y2 - 1)

dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

# 승객을 다 태울때까지
while passenger:
    # 승객 전체와의 거리 구함 (승객 좌표, 거리)
    tmp_lst = bfs(now_loc, passenger.keys())
    # 거리가 가장 가까운 > 행 작은 > 열 작은 승객에게 출발
    if tmp_lst:
        tmp_lst.sort(key=lambda x: (x[2], x[0], x[1]))
        x, y, d = tmp_lst[0]
        loc = (x, y)
    else:
        F = -1
        break

    # 도착 좌표 설정
    target_loc = [passenger.pop(loc)]
    now_loc = loc
    F -= d

    # 출발점 - 도착점 거리 구함, 가능하면 움직이고 연료 충전
    tg = bfs(now_loc, target_loc)
    if not tg:
        F = -1
        break

    now_loc = target_loc[0]
    F = F - tg[0][2] + 2 * tg[0][2]

print(F)


"""
연료가 바닥날때까지
    승객 전체와의 거리 구함 (거리, 좌표)
    거리가 가장 가까운 > 행 작은 > 열 작은 승객에게 출발
    출발점 - 도착점 거리 구함, 출발

최단거리이므로 bfs로 접근
각 승객에 대해서 모두 각각의 bfs를 돌리려고 하다가 시간초과 발생
한 번에 모든 좌표를 다 돌고 비교만 하면 됨
"""
