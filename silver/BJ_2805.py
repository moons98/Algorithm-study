# -*- coding: utf-8 -*-
import sys

N, M = map(int, sys.stdin.readline().split())
tree = list(map(int, sys.stdin.readline().split()))
tree.sort()

start, end = 0, tree[-1]
while start <= end:
    mid = (start + end) // 2
    left_tree = 0
    for i in tree:
        if i >= mid:
            left_tree += i - mid

    if left_tree >= M:
        start = mid + 1
    else:
        end = mid - 1
print(end)

"""
정렬 후, 이분탐색으로 찾으면 그 값보다 큰 값은 전체 합에서 뺀 만큼 잘릴 것
-> 시간 초과 발생, 단순 for문으로 돌게끔
"""
