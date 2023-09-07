# -*- coding: utf-8 -*-
import sys
from bisect import bisect_left

N = int(sys.stdin.readline())
num = list(map(int, sys.stdin.readline().split()))

lst = [num[0]]
for i in num[1:]:
    if lst[-1] < i:
        lst.append(i)
    else:
        loc = bisect_left(lst, i)
        lst[loc] = i

print(len(lst))

"""
7
10 20 -10 30 -5 10 25 
"""
