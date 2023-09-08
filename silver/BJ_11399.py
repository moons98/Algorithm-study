# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
time = list(map(int, sys.stdin.readline().split()))
time.sort()

add_time = [0 for _ in time]
for i in range(len(time)):
    if i == 0:
        add_time[i] = time[i]
    else:
        add_time[i] = time[i] + add_time[i - 1]

print(sum(add_time))
