# -*- coding: utf-8 -*-
import sys

sys.setrecursionlimit(10**6)  # 안써주면 런타임 에러 발생


def dfs(x, y, rain):
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
            dfs(nx, ny, rain)

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
                dfs(x, y, i)
                result += 1

    answer = max(answer, result)

print(answer)
