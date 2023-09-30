# -*- coding: utf-8 -*-
import sys
from collections import deque


def rotate(x, y, L):
    tmp = [[map_lst[x + j][y + i] for i in range(L)] for j in range(L)]
    for i in range(L):
        for j in range(L):
            map_lst[x + j][y + L - i - 1] = tmp[i][j]

    return


def remove_ice():
    tmp = [i[:] for i in map_lst]

    for x in range(2**N):
        for y in range(2**N):
            if map_lst[x][y] != 0:
                ice = 4
                for i in range(4):
                    nx = x + dx[i]
                    ny = y + dy[i]
                    if nx < 0 or nx >= 2**N or ny < 0 or ny >= 2**N:
                        ice -= 1
                    elif map_lst[nx][ny] == 0:
                        ice -= 1

                if ice < 3:
                    tmp[x][y] = map_lst[x][y] - 1

    return tmp


def bfs():
    visited = [[0 for _ in range(2**N)] for _ in range(2**N)]
    max_area = 0

    for x in range(2**N):
        for y in range(2**N):
            if not visited[x][y] and map_lst[x][y] != 0:
                visited[x][y] = 1
                queue = deque([[x, y]])
                tmp_area = 1
                while queue:
                    x, y = queue.popleft()
                    for i in range(4):
                        nx, ny = x + dx[i], y + dy[i]
                        if 0 <= nx < 2**N and 0 <= ny < 2 ** N and map_lst[nx][ny] != 0 and not visited[nx][ny]:
                            queue.append([nx, ny])
                            visited[nx][ny] = 1
                            tmp_area += 1

                max_area = max(max_area, tmp_area)

    return max_area


N, Q = map(int, sys.stdin.readline().split())
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(2**N)]

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

magic = list(map(int, sys.stdin.readline().split()))
for i in range(Q):
    part = 2 ** magic[i]
    if part != 1:
        for x in range(0, 2**N, part):
            for y in range(0, 2**N, part):
                rotate(x, y, part)

    map_lst = remove_ice()

print(sum([sum(i) for i in map_lst]))
print(bfs())

"""
deepcopy issue 주의!
tmp = [i[:] for i in map_lst] # deepcopy
tmp = map_lst[::] # copy
"""
