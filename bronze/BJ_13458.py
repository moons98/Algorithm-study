# -*- coding: utf-8 -*-
import math
import sys

N = int(sys.stdin.readline())

candidate = list(map(int, sys.stdin.readline().split()))
B, C = map(int, sys.stdin.readline().split())

answer = 0
for i in candidate:
    answer += 1 if i <= B else int(math.ceil(float(i - B) / C) + 1)

print(answer)
