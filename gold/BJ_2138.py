# -*- coding: utf-8 -*-
import sys
from math import inf


def change(A, B):
    A_copy = A[:]
    press = 0

    for i in range(1, len(A)):
        if A_copy[i - 1] == B[i - 1]:
            continue
        else:
            press += 1
            for j in range(i - 1, min(i + 2, len(A_copy))):
                A_copy[j] = 1 - A_copy[j]

    return press if A_copy == B else inf


N = int(sys.stdin.readline())
state = [[int(j) for j in sys.stdin.readline().rstrip()] for _ in range(2)]

# 맨 앞을 바꾸는 경우와 그렇지 않은 경우 구분
press_start = state[0][:]
press_start[0] = 1 - press_start[0]
press_start[1] = 1 - press_start[1]

answer = min(change(*state), change(press_start, state[1]) + 1)
if answer != inf:
    print(answer)
else:
    print(-1)
