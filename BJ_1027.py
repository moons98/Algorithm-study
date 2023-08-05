# -*- coding: utf-8 -*-
import sys
from math import inf


def cal_slope(x1, x2, y1, y2):
    return (x2 - x1) / (y2 - y1) if y1 != y2 else 0


answer = 0
num_building = int(input())
building = list(map(float, sys.stdin.readline().split()))

for idx, val in enumerate(building):
    tmp = 0
    left, right = inf, -inf
    # cal_left
    for i in range(idx - 1, -1, -1):
        slope = cal_slope(val, building[i], idx, i)
        if slope < left:
            tmp += 1
            left = slope
    # cal_right
    for i in range(idx + 1, num_building):
        slope = cal_slope(val, building[i], idx, i)
        if slope > right:
            tmp += 1
            right = slope
    if tmp > answer:
        answer = tmp

print(answer)
