# -*- coding: utf-8 -*-
import copy
import sys


def light_map(arr, i, x, y):
    for idx in i:
        nx, ny = x, y
        while True:
            nx += loc[idx][0]
            ny += loc[idx][1]
            if 0 > nx or nx >= N or 0 > ny or ny >= M or arr[nx][ny] == 6:
                break
            elif arr[nx][ny] == 0:
                arr[nx][ny] = -1

    return


def dfs(arr, d):
    global min_value

    if d == len(cctv):
        cnt = 0
        for i in range(N):
            cnt += arr[i].count(0)
        min_value = min(min_value, cnt)
        return

    tmp_map = copy.deepcopy(arr)
    x, y, val = cctv[d]
    for i in graph[val]:
        light_map(tmp_map, i, x, y)
        dfs(tmp_map, d + 1)

        # dfs 끝난 뒤에는 이전의 map에서 시작
        tmp_map = copy.deepcopy(arr)

    return


N, M = map(int, sys.stdin.readline().split())

map_lst, cctv = [], []
for x in range(N):
    tmp = list(map(int, sys.stdin.readline().split()))
    for y in range(M):
        if 1 <= tmp[y] <= 5:
            cctv.append([x, y, tmp[y]])

    map_lst.append(tmp)

loc = [(0, 1), (-1, 0), (0, -1), (1, 0)]
graph = [
    [],
    [[0], [1], [2], [3]],
    [[0, 2], [1, 3]],
    [[0, 1], [1, 2], [2, 3], [3, 0]],
    [[0, 1, 2], [1, 2, 3], [2, 3, 0], [3, 0, 1]],
    [[0, 1, 2, 3]],
]

min_value = int(1e9)
dfs(map_lst, 0)

print(min_value)


"""
cctv 영역 넓은곳부터 map_lst를 가장 많이 밝힐수 있는 방향으로 비추기
1. 방향 정하기
2. 비추기
"""
