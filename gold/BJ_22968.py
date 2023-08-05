# -*- coding: utf-8 -*-
import sys

T = int(sys.stdin.readline())

answer = []
for i in range(T):
    V = int(sys.stdin.readline())

    if V < 3:
        answer.append(V)
    else:
        n1, n2, h = 2, 1, 3
        tmp = n1 + n2 + 1
        while tmp <= V:
            n2 = n1
            n1 = tmp
            tmp = n2 + n1 + 1
            if tmp <= V:
                h += 1
            else:
                break

        answer.append(h)

for i in answer:
    print(i)

"""
점화식을 찾아서 풀 수 있었어야 함
"""
