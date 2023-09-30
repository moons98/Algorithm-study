# -*- coding: utf-8 -*-
import sys


def tornado(x, y, idx):
    global map_lst
    nx = x + dx[idx]
    ny = y + dy[idx]
    sand = map_lst[nx][ny]
    tmp = sand

    # 방향 설정
    left = (idx + 1) % 4
    right = (idx - 1) % 4
    top = idx
    bottom = (idx + 2) % 4

    for i in [left, right]:
        # 7% 구간
        tx = nx + dx[i]
        ty = ny + dy[i]
        fly_sand = int(sand * 0.07)
        if 0 <= tx < N and 0 <= ty < N:
            map_lst[tx][ty] += fly_sand
        tmp -= fly_sand

        for r, j in zip([0.02, 0.1, 0.01], [i, top, bottom]):
            rx = tx + dx[j]
            ry = ty + dy[j]
            fly_sand = int(sand * r)

            if 0 <= rx < N and 0 <= ry < N:
                map_lst[rx][ry] += fly_sand
            tmp -= fly_sand

    # 5% 구간
    tx = nx + dx[idx] * 2
    ty = ny + dy[idx] * 2
    fly_sand = int(sand * 0.05)
    if 0 <= tx < N and 0 <= ty < N:
        map_lst[tx][ty] += fly_sand
    tmp -= fly_sand

    # a 구간
    tx = nx + dx[idx]
    ty = ny + dy[idx]
    if 0 <= tx < N and 0 <= ty < N:
        map_lst[tx][ty] += tmp

    map_lst[nx][ny] = 0

    return nx, ny


N = int(sys.stdin.readline())
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
total = sum([sum(i) for i in map_lst])

dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]

idx, rep = 0, 1
x, y = N // 2, N // 2

# 달팽이 배열
while (x, y) != (0, 0):
    # 11223344식으로 반복횟수 증가
    for _ in range(2):
        for _ in range(rep):
            if not (x, y) == (0, 0):
                x, y = tornado(x, y, idx)
        idx = (idx + 1) % 4
    rep += 1

answer = total - sum([sum(i) for i in map_lst])
print(answer)
