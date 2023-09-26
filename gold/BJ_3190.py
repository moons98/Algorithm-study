# -*- coding: utf-8 -*-
import sys
from collections import deque


def dummy(directions):
    answer = 0
    body = deque([[0, 0]])

    cur_dir = 1
    while True:
        nx, ny = body[-1][0] + dx[cur_dir], body[-1][1] + dy[cur_dir]
        answer += 1

        # 머리 처리
        if nx < 0 or nx >= N or ny < 0 or ny >= N:
            return answer
        elif [nx, ny] in body:
            return answer
        else:
            body.append([nx, ny])

        # 꼬리 처리
        if graph[nx][ny] == 0:
            body.popleft()
        else:
            graph[nx][ny] = 0

        # 방향 조절
        if directions and answer in directions.keys():
            if directions[answer] == "D":
                cur_dir = (cur_dir - 1) % 4
            elif directions[answer] == "L":
                cur_dir = (cur_dir + 1) % 4

            directions.pop(answer)


N = int(sys.stdin.readline())
K = int(sys.stdin.readline())

# 사용하는 칸은  NxN 기준으로 0~N 까지의 좌표를 사용
graph = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
for _ in range(K):
    x, y = map(int, sys.stdin.readline().split())
    graph[x - 1][y - 1] = 1

L = int(sys.stdin.readline())
directions = dict()
for _ in range(L):
    X, C = map(str, sys.stdin.readline().split())
    directions[int(X)] = C

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]
print(dummy(directions))

"""
문제가 좀 모호한 부분이 있는듯
NxN이면 점의 갯수는 N+1개가 있을탠데, 정답은 N개

dict type으로 방향전환을 시키는 방법 생각할 수 있음
방향전환이 시작시간 기준으로 나와있음 주의
"""
