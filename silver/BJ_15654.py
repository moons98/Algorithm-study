# -*- coding: utf-8 -*-
import sys

N, M = map(int, sys.stdin.readline().split())
tmp = set(map(int, sys.stdin.readline().split()))
num = sorted(list(tmp))
answer = []


def dfs(depth):
    if depth == M:
        print(" ".join(map(str, answer)))
        return

    for i in range(N):
        if num[i] in answer:
            continue
        else:
            answer.append(num[i])
            dfs(depth + 1)
            answer.pop()


dfs(0)


"""
back-tracking, 재귀
"""
