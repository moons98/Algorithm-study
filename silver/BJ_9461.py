# -*- coding: utf-8 -*-
import sys

T = int(sys.stdin.readline())

P = [1, 1, 1]
tmp = [1, 1, 1]
idx = 0
for i in range(100):
    new_val = sum(tmp) - tmp[idx]
    P.append(new_val)
    idx = (idx + 1) % 3
    tmp[idx] = new_val


answer = []
for i in range(T):
    N = int(sys.stdin.readline())
    answer.append(P[N - 1])

for i in answer:
    print(i)
