# -*- coding: utf-8 -*-
import sys
from collections import deque


def bfs():
    global idx_lst

    idx = 0
    num_dict = dict()

    visited = [[0 for _ in range(n)] for _ in range(n)]
    for tx in range(n):
        for ty in range(n):
            # 방문하지 않은 좌표면 새로운 인덱스 i 부여하고 탐색 시작
            if visited[tx][ty] == 0:
                total_sum, total_area = map_lst[tx][ty], 1
                idx += 1
                visited[tx][ty] = idx

                queue = deque()
                queue.append([tx, ty])
                while queue:
                    x, y = queue.popleft()
                    for i in range(4):
                        nx = x + dx[i]
                        ny = y + dy[i]

                        if nx < 0 or nx >= n or ny < 0 or ny >= n:
                            continue
                        elif visited[nx][ny]:
                            continue
                        elif l <= abs(map_lst[x][y] - map_lst[nx][ny]) <= r:
                            visited[nx][ny] = idx
                            queue.append([nx, ny])

                            total_area += 1
                            total_sum += map_lst[nx][ny]

                # 값 계산 후 dict update
                num_dict[idx] = total_sum // total_area

    if idx == n**2:
        return False

    for x in range(n):
        for y in range(n):
            map_lst[x][y] = num_dict[visited[x][y]]

    return True


n, l, r = map(int, sys.stdin.readline().split())

map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]
idx_lst = [[0 for _ in range(n)] for _ in range(4)]

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

answer = 0
while bfs():
    answer += 1

print(answer)
