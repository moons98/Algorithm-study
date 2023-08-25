# -*- coding: utf-8 -*-
import sys
from collections import deque

A, B = map(int, sys.stdin.readline().split())

count = 0
while B > A:
    if B % 2 == 0:
        B /= 2
        count += 1
    elif B % 10 == 1:
        B //= 10
        count += 1
    else:
        break

if B == A:
    print(count + 1)
else:
    print(-1)

"""
방법1 : B->A로 가는 top-down 방식
"""


def bfs():
    queue = deque()
    queue.append([A, 0])
    while queue:
        num, trial = queue.popleft()
        if num < B:
            queue.append([num * 2, trial + 1])
            queue.append([int(str(num) + "1"), trial + 1])
        elif num == B:
            return trial + 1

    return -1


# print(bfs())

"""
방법2 : bfs를 이용한 bottom-up 방식
"""
