# -*- coding: utf-8 -*-
import sys

T = int(sys.stdin.readline())
answer = []
for i in range(T):
    n = int(sys.stdin.readline())
    case = [list(map(int, sys.stdin.readline().split())) for _ in range(2)]

    for i in range(1, n):
        if i < 2:
            case[0][i] += case[1][i - 1]
            case[1][i] += case[0][i - 1]
        else:
            case[0][i] = max(case[1][i - 1] + case[0][i], case[1][i - 2] + case[0][i])
            case[1][i] = max(case[0][i - 1] + case[1][i], case[0][i - 2] + case[1][i])

    answer.append(max(case[0][-1], case[1][-1]))

for i in answer:
    print(i)
