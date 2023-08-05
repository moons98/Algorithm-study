# -*- coding: utf-8 -*-
import sys
from collections import deque

# BFS, queue, 최단경로
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]


def BFS(place, loc):
    bundle = 0
    queue = deque()

    for loc_x, loc_y in loc:
        if place[loc_x][loc_y] == 1:
            queue.append([loc_x, loc_y])
            while queue:
                x, y = queue.popleft()
                # place[x][y] += 1
                for i in range(4):
                    nx = x + dx[i]
                    ny = y + dy[i]
                    if 0 <= nx <= N - 1 and 0 <= ny <= M - 1 and place[nx][ny] == 1:
                        queue.append([nx, ny])
                        place[nx][ny] += 1
                        # 방문 처리를 넣는 순간에 해줘야 함
                        # 그렇지 않으면 BFS로 같은 깊이 구간들 도는 동안에 중복된 좌표 입력될 수 있음
            bundle += 1

    return bundle


# Main
num_case = int(sys.stdin.readline())
ans_lst = []
for i in range(num_case):
    M, N, K = map(int, sys.stdin.readline().split())
    place = [[0 for m in range(M)] for n in range(N)]  # 0부터 index가 시작함

    loc = list()
    for j in range(K):
        y, x = map(int, sys.stdin.readline().split())
        loc.append([x, y])
        place[x][y] = 1

    answer = BFS(place, loc)
    ans_lst.append(answer)

for i in ans_lst:
    print(i)
