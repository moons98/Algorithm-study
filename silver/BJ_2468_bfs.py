# -*- coding: utf-8 -*-
import sys
from collections import deque


def bfs(x, y, rain):
    queue = deque([[x, y]])
    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue
            elif visited[nx][ny] == 1:
                continue
            elif map_lst[nx][ny] <= rain:
                continue
            else:
                visited[nx][ny] = 1
                queue.append([nx, ny])

    return


N = int(sys.stdin.readline())
max_rain = 0
map_lst = []
for _ in range(N):
    tmp = list(map(int, sys.stdin.readline().split()))
    max_rain = max(max_rain, max(tmp))
    map_lst.append(tmp)

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

answer = 0
for i in range(max_rain):
    visited = [[0 for _ in range(N)] for _ in range(N)]
    result = 0
    for x in range(N):
        for y in range(N):
            if map_lst[x][y] > i and visited[x][y] == 0:
                bfs(x, y, i)
                result += 1

    answer = max(answer, result)

print(answer)
