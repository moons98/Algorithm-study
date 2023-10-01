# -*- coding: utf-8 -*-
import sys
from collections import deque


def bfs(shark, size):
    queue = deque([[shark[0], shark[1], 0]])
    distance = [[0 for _ in range(N)] for _ in range(N)]

    dis = 0
    loc = set()
    while queue:
        x, y, d = queue.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= N or ny < 0 or ny >= N or distance[nx][ny]:
                continue
            elif map_lst[nx][ny] == 0 or map_lst[nx][ny] == size:
                distance[nx][ny] = d + 1
                queue.append([nx, ny, d + 1])
            # 사이즈가 같으면 먹을수는 없지만, 지나갈 수는 있음
            elif map_lst[nx][ny] < size and map_lst[nx][ny] <= 6:
                if dis == 0:
                    loc.add((nx, ny))
                    dis = d + 1
                elif d + 1 == dis:
                    loc.add((nx, ny))

    if loc:
        lst_set = sorted(list(loc), key=lambda x: (x[0], x[1]))
    else:
        lst_set = [(0, 0)]

    return lst_set[0], dis


N = int(sys.stdin.readline())

map_lst = []
for i in range(N):
    tmp = list(map(int, sys.stdin.readline().split()))
    for j, val in enumerate(tmp):
        if val == 9:
            shark = [i, j]
    map_lst.append(tmp)

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

size = 2
num_fish = 2
answer = 0

while True:
    new_loc, time = bfs(shark, size)
    if not time:
        break
    else:
        map_lst[shark[0]][shark[1]] = 0
        map_lst[new_loc[0]][new_loc[1]] = 9
        shark = new_loc
        answer += time
        num_fish -= 1
        if num_fish == 0:
            size += 1
            num_fish = size

print(answer)

"""
문제 조건을 정확히 파악하고 들어가야 함
나중에 구현하고 조건을 다르게 이해해서 시간낭비함
"""
