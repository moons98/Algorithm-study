# -*- coding: utf-8 -*-
import sys
from collections import deque


def bfs():
    queue = deque([[S, 0]])
    visited = [0 for _ in range(F + 1)]
    while queue:
        [tmp_stair, trial] = queue.popleft()
        if tmp_stair == G:
            return trial

        for i in [U, -D]:
            check_stair = tmp_stair + i
            if 1 > check_stair or check_stair > F or visited[check_stair]:
                continue

            queue.append([check_stair, trial + 1])
            visited[check_stair] = 1

    return -1


F, S, G, U, D = map(int, sys.stdin.readline().split())

answer = bfs()
if answer == -1:
    print("use the stairs")
else:
    print(answer)

"""
tmp_stair을 가지고 U/D을 모두 체크해서 층이 변하는 문제
"""
