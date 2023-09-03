# -*- coding: utf-8 -*-
import sys

N, r, c = map(int, sys.stdin.readline().split())

loc = []
std = 2**N
while std >= 2:
    tmp_loc = 1
    if std / 2 <= r < std:
        tmp_loc += 2
        r -= std / 2
    if std / 2 <= c < std:
        tmp_loc += 1
        c -= std / 2
    loc.append(tmp_loc)
    std /= 2

answer = 0
for idx, num in enumerate(loc[::-1]):
    answer += (2**idx) ** 2 * (num - 1)

print(answer)
