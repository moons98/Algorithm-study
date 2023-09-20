# -*- coding: utf-8 -*-
import sys
from collections import deque


def bfs(red, blue, val):
    queue = deque()
    queue.append([red, blue, val])

    visited = set()
    visited.add((red[0], red[1], blue[0], blue[1]))
    while queue:
        R, B, val = queue.popleft()
        for i in range(4):
            rx, ry = R[0], R[1]
            bx, by = B[0], B[1]

            # Red 구슬 움직이기
            red_move = 0
            while True:
                rx += dx[i]
                ry += dy[i]
                red_move += 1

                if map_lst[rx][ry] == "#":
                    rx -= dx[i]
                    ry -= dy[i]
                    red_move -= 1
                    break
                elif map_lst[rx][ry] == "O":
                    break

            # Blue 구슬 움직이기
            blue_move = 0
            while True:
                bx += dx[i]
                by += dy[i]
                blue_move += 1

                if map_lst[bx][by] == "#":
                    bx -= dx[i]
                    by -= dy[i]
                    blue_move -= 1
                    break
                elif map_lst[bx][by] == "O":
                    break

            # 예제 7, 두 구슬이 모두 떨어지는 경우는 -1
            if map_lst[bx][by] == "O":
                continue

            # 경우의 수 분석
            if rx == bx and ry == by:
                if red_move < blue_move:
                    bx -= dx[i]
                    by -= dy[i]
                else:
                    rx -= dx[i]
                    ry -= dy[i]

            if map_lst[rx][ry] == "O":
                return val + 1

            # visited로 전에 방문한 적 있는지 확인, 최단거리만 필요하기 때문
            if val + 1 < 10 and (rx, ry, bx, by) not in visited:
                queue.append([[rx, ry], [bx, by], val + 1])
                visited.add((rx, ry, bx, by))

    return -1


N, M = map(int, sys.stdin.readline().split())
map_lst = [[j for j in map(str, sys.stdin.readline().strip())] for _ in range(N)]

for i in range(N):
    for j in range(M):
        if map_lst[i][j] == "R":
            red = [i, j]
        elif map_lst[i][j] == "B":
            blue = [i, j]

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]
print(bfs(red, blue, 0))

"""
최소 횟수이므로 bfs
R,B가 겹치는 경우 움직임을 횟수로 구분
구슬이 둘 다 떨어지는 경우 -1 출력해야 함
visited 사용해서 중복된 좌표는 고려하지 않도록 함
"""
