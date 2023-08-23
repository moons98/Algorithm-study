# -*- coding: utf-8 -*-
import sys

n = int(sys.stdin.readline())
triangle = [list(map(int, sys.stdin.readline().split()))]

for i in range(1, n):
    tmp = list(map(int, sys.stdin.readline().split()))
    for j in range(i + 1):
        target = triangle[i - 1]
        if j == 0:
            tmp[j] += target[j]
        else:
            tmp[j] += max(target[j - 1 : j + 1])

    triangle.append(tmp)
    target = tmp

print(max(triangle[-1]))
