# -*- coding: utf-8 -*-
import sys


def magic(d, s):
    global cloud, map_lst
    loc = set()

    # 구름 이동, 비내리기
    for x, y in cloud:
        nx = (x + dir[d][0] * s) % N
        ny = (y + dir[d][1] * s) % N

        map_lst[nx][ny] += 1
        loc.add((nx, ny))

    # 물복사버그 마법
    for x, y in loc:
        for i in [1, 3, 5, 7]:
            nx, ny = x + dir[i][0], y + dir[i][1]
            if 0 <= nx < N and 0 <= ny < N and map_lst[nx][ny]:
                map_lst[x][y] += 1

    # 구름 생성
    cloud = set()
    for i in range(N):
        for j in range(N):
            if map_lst[i][j] >= 2:
                cloud.add((i, j))

    cloud = cloud - loc
    for i, j in cloud:
        map_lst[i][j] -= 2

    return


N, M = map(int, sys.stdin.readline().split())
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
order = [list(map(int, sys.stdin.readline().split())) for _ in range(M)]

dir = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]

cloud = set(((N - 1, 0), (N - 1, 1), (N - 2, 0), (N - 2, 1)))
for d, s in order:
    magic(d - 1, s)

print(sum([sum(i) for i in map_lst]))

"""
시간 초과: 생성된 구름이 기존에 있던 좌표인지 확인하는 과정에서 (i,j) in loc을 사용해서 생긴 문제
cloud를 set 자료구조 활용해서 운용
"""
