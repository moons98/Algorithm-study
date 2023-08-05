# -*- coding: utf-8 -*-
import sys


def find_next_num(num):
    start = len(num) - 1  # 3자리면 2
    if len(num) == 0:
        return "BIGGEST"
    while num[start - 1] >= num[start] and start >= 1:
        start -= 1
        if start == 0:
            return "BIGGEST"
    num_left = sorted(num[start - 1 :], reverse=True)  # 내림차순으로 정렬, 후에 index로 큰 수 찾으려고
    idx = num_left.index(num[start - 1]) - 1

    tmp = num_left.pop(idx)
    next_num = num[: start - 1] + [tmp] + num_left[::-1]

    return "".join(map(str, next_num))


answer = []
N = int(sys.stdin.readline())
for _ in range(N):
    num = list(map(int, sys.stdin.readline().strip()))
    answer.append(find_next_num(num))

for i in answer:
    print(i)

"""
1
279134399742
"""
