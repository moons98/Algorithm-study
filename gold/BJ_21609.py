# -*- coding: utf-8 -*-
import sys
from collections import deque


def find_block():
    """
    1. 크기가 가장 큰 블록 그룹을 찾는다.
    - 포함된 무지개 블록의 수가 가장 많은 블록 그룹
    - 기준 블록의 행이 가장 큰 것 (무지개 블록이 아닌 것 중, 행/열 순으로 가장 작은 것)
    - 열이 가장 큰 것
    """
    block_group = dict()
    total = 0

    visited = [[0 for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if visited[x][y] or map_lst[x][y] <= 0:
                continue

            color = map_lst[x][y]
            tmp_group = dict({0: [], 1: [[x, y]]})
            tmp_total = 1

            queue = deque([[x, y]])
            visited[x][y] = 1
            while queue:
                tx, ty = queue.popleft()
                for i in range(4):
                    nx, ny = tx + dir[i][0], ty + dir[i][1]
                    if 0 > nx or nx >= N or 0 > ny or ny >= N or visited[nx][ny] or (map_lst[nx][ny] not in (color, 0)):
                        continue

                    queue.append([nx, ny])
                    visited[nx][ny] = 1

                    if map_lst[nx][ny] == 0:
                        tmp_group[0].append([nx, ny])
                    else:
                        tmp_group[1].append([nx, ny])
                    tmp_total += 1

            # 그룹 블록의 구성이 2개 이하면 넘기기
            if tmp_total < 2:
                pass
            # 크기가 가장 큰 블록 그룹
            elif tmp_total > total:
                block_group = tmp_group
                total = tmp_total
            elif tmp_total == total:
                # 무지개 블록의 수가 가장 많은 블록
                if len(tmp_group[0]) > len(block_group[0]):
                    block_group = tmp_group
                    total = tmp_total
                elif len(tmp_group[0]) == len(block_group[0]):
                    # 기준 블록 찾기
                    block_group[1].sort(key=lambda x: (x[0], x[1]))
                    tmp_group[1].sort(key=lambda x: (x[0], x[1]))
                    # 기준블록의 행이 큰 그룹
                    if tmp_group[1][0][0] > block_group[1][0][0]:
                        block_group = tmp_group
                        total = tmp_total
                    # 기준블록의 열이 큰 그룹
                    elif tmp_group[1][0][0] == block_group[1][0][0] and tmp_group[1][0][1] > block_group[1][0][1]:
                        block_group = tmp_group
                        total = tmp_total

            for i, j in tmp_group[0]:
                visited[i][j] = 0

    return block_group, total if total >= 2 else False


def remove_block(block, total):
    global answer
    answer += total**2

    for i in block:
        for x, y in block[i]:
            map_lst[x][y] = -2

    return


def gravity():
    for x in range(N - 1, -1, -1):
        for y in range(N):
            if map_lst[x][y] >= 0:
                nx, ny = x, y
                color = map_lst[x][y]
                while True:
                    nx += dir[1][0]
                    ny += dir[1][1]

                    if 0 > nx or nx >= N or 0 > ny or ny >= N or map_lst[nx][ny] >= -1:
                        nx -= dir[1][0]
                        ny -= dir[1][1]
                        break

                map_lst[x][y] = -2
                map_lst[nx][ny] = color

    return


def rotate_block():
    global map_lst

    new_map = [[0 for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            new_map[N - 1 - y][x] = map_lst[x][y]

    map_lst = new_map


N, M = map(int, sys.stdin.readline().split())
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]

answer = 0
while True:
    block, total = find_block()
    if not total:
        break
    else:
        remove_block(block, total)
        gravity()
        rotate_block()
        gravity()

print(answer)

"""
일반 블록은 M가지 색상이 있고, 색은 M이하의 자연수로 표현
검은색 블록은 -1, 무지개 블록은 0으로 표현

1. 크기가 가장 큰 블록 그룹을 찾는다. 
  - 포함된 무지개 블록의 수가 가장 많은 블록 그룹
  - 기준 블록의 행이 가장 큰 것 (무지개 블록이 아닌 것 중, 행/열 순으로 가장 작은 것)
  - 열이 가장 큰 것
2. 1에서 찾은 블록 그룹의 모든 블록을 제거 
  - (블록 그룹에 포함된 블록의 수 **2)점을 획득
3. 격자에 중력이 작용
  - 검은색 블록을 제외한 모든 블록이 행의 번호가 큰 칸으로 이동.
  - 다른 블록이나 격자를 만나기 전까지 계속됨
4. 격자가 90도 반시계 방향으로 회전
5. 다시 격자에 중력이 작용

블록 그룹에 속하는 일반 블럭의 색이 같아야 한다는 조건을 놓침
반시계 회전 좌표를 놓침
if문 사용에서 조건을 잘못 걸어줌 (앞의 조건이 틀리면 가도록 elif문을 써야 하는데, else로 퉁침)
"""
