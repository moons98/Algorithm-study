# -*- coding: utf-8 -*-
import sys


def check_avail(arr):
    for idx, val in enumerate(arr):
        if val > N:
            return False
        while cnt[val] == 1:
            val += K
            if val > N:
                return False
        cnt[val] = 1

    return True


N, K = map(int, sys.stdin.readline().split())
arr = list(map(int, sys.stdin.readline().split()))
arr.sort()
cnt = [0 for _ in range(N + 1)]

result = check_avail(arr)


if result:
    print(1)
else:
    print(0)

"""
5 2
1 2 2 3 5
"""
