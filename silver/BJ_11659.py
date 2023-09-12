# -*- coding: utf-8 -*-
import sys

N, M = map(int, sys.stdin.readline().split())
num = [0] + list(map(int, sys.stdin.readline().split()))

for i in range(1, N + 1):
    num[i] = num[i - 1] + num[i]

answer = []
for i in range(M):
    i, j = map(int, sys.stdin.readline().split())
    answer.append(num[j] - num[max(i - 1, 0)])

for i in answer:
    print(i)
