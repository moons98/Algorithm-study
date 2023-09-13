# -*- coding: utf-8 -*-
import sys
from collections import deque

M, N = map(int, sys.stdin.readline().split())
map_lst = list(list(map(int, sys.stdin.readline().split())) for _ in range(N))

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

queue = deque()
for idx1, val1 in enumerate(map_lst):
    for idx2, val2 in enumerate(val1):
        if val2 == 1:
            queue.append([idx1, idx2])
queue.append([-1, -1])

answer = -1
while queue:
    x, y = queue.popleft()
    if x == -1 and y == -1:
        if queue:
            queue.append([-1, -1])
        answer += 1
    else:
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if nx < 0 or nx > N - 1 or ny < 0 or ny > M - 1:
                continue
            elif map_lst[nx][ny] == 0:
                queue.append([nx, ny])
                map_lst[nx][ny] = 1

for idx1, val1 in enumerate(map_lst):
    for idx2, val2 in enumerate(val1):
        if val2 == 0:
            answer = -1
            break

print(answer)

"""
python3로 실행할 때와 python으로 실행할 때 차이로 TypeError 발생
-> list(map(int, sys.stdin.readline().split())) for _ in range(N)에서 list() 안감싸줘서 map 객체로 전달된 문제
"""
