# -*- coding: utf-8 -*-
import copy
import sys


def diffusion():
    global map_lst

    new_map = copy.deepcopy(map_lst)
    for x in range(r):
        for y in range(c):
            dust = map_lst[x][y]
            diff = dust // 5

            if dust == -1:
                continue

            # 4방향 이동 검사
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]

                if nx < 0 or nx >= r or ny < 0 or ny >= c:
                    continue
                elif map_lst[nx][ny] == -1:
                    continue

                new_map[nx][ny] += diff
                new_map[x][y] -= diff

    map_lst = new_map

    return


def work():
    global map_lst

    new_map = copy.deepcopy(map_lst)

    for (x, y), dir_x in zip(air_conditioner, [upper_dx, lower_dx]):
        d = 0
        while d <= 3:
            nx = x + dir_x[d]
            ny = y + upper_dy[d]

            # 좌표 확인
            if nx < 0 or nx >= r or ny < 0 or ny >= c or map_lst[nx][ny] == -1:
                d += 1
                continue

            # 값 밀어내기
            if map_lst[x][y] == -1:
                new_map[nx][ny] = 0
            else:
                new_map[nx][ny] = map_lst[x][y]

            x, y = nx, ny

    map_lst = new_map

    return


"""
공기청정기는 항상 1번 열에 설치, 두 행 차지

1. 미세먼지 확산
    - 모든 칸에서 동시에 일어남
    - 인접한 네 방향으로 확산
    - 인접한 방향에 공기청정기가 있거나, 칸이 없으면 확산 x
    - 확산되는 양은 A//5, 남은 양은 원본 - 확산된 먼지

2. 공기청정기 작동
    - 위쪽의 바람은 반시계 순환, 아래쪽 바람은 시계방향
    - 미세먼지가 바람 방향대로 한 칸씩 이동
"""

r, c, t = map(int, sys.stdin.readline().split())

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

upper_dx = [0, -1, 0, 1]
upper_dy = [1, 0, -1, 0]

lower_dx = [0, 1, 0, -1]

map_lst = []
air_conditioner = []
for i in range(r):
    row = list(map(int, sys.stdin.readline().split()))
    if row[0] == -1:
        air_conditioner.append((i, 0))

    map_lst.append(row)

for _ in range(t):
    diffusion()
    work()

print(sum([sum(i) for i in map_lst]) + 2)
