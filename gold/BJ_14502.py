# -*- coding: utf-8 -*-
import sys
import copy

from collections import deque
from itertools import combinations


def count_zeros(map_lst):
    global answer

    tmp_answer = 0
    for i in range(N):
        tmp_answer += map_lst[i].count(0)

    answer = max(answer, tmp_answer)

    return


def bfs(tmp_lst):
    queue = deque(virus_loc)
    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            # 움직일 수 없는 경우
            if nx < 0 or nx >= N or ny < 0 or ny >= M:
                continue
            elif tmp_lst[nx][ny] == 0:
                tmp_lst[nx][ny] = 2
                queue.append([nx, ny])

    count_zeros(tmp_lst)

    return


def make_wall_comb():
    wall_loc = list(combinations(zeros_loc, 3))
    for i in wall_loc:
        tmp_lst = copy.deepcopy(map_lst)
        for x, y in i:
            tmp_lst[x][y] = 1

        bfs(tmp_lst)

    return


N, M = map(int, sys.stdin.readline().split())
answer = 0

map_lst = []
virus_loc, zeros_loc = [], []
for x in range(N):
    tmp = list(map(int, sys.stdin.readline().split()))
    for y, num in enumerate(tmp):
        if num == 2:
            virus_loc.append([x, y])
        if not num:
            zeros_loc.append([x, y])

    map_lst.append(tmp)

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

make_wall_comb()
print(answer)

"""
전체 퍼지는 곳을 다 처리해야 하므로 bfs, deque
가짓수가 많지 않으므로 전체 벽을 세울 수 있는 경우를 모두 체크하며 bfs 돌기
어짜피 brute-force하게 벽을 세워야 하므로, 이중 for문 대신에 조합 사용해서 시간 단축
"""

"""
def bfs():
    queue = deque(virus_loc)
    tmp_lst = copy.deepcopy(map_lst)
    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            # 움직일 수 없는 경우
            if nx < 0 or nx >= N or ny < 0 or ny >= M:
                continue
            elif tmp_lst[nx][ny] == 0:
                tmp_lst[nx][ny] = 2
                queue.append([nx, ny])

    count_zeros(tmp_lst)

    return


def make_wall(cnt):
    if cnt == 3:
        bfs()
        return
    for x in range(N):
        for y in range(M):
            if map_lst[x][y] == 0:
                map_lst[x][y] = 1
                make_wall(cnt + 1)
                map_lst[x][y] = 0

"""
