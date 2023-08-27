# -*- coding: utf-8 -*-
import sys

N, M = map(int, sys.stdin.readline().split())
num = sorted(list(set(map(int, sys.stdin.readline().split()))))
answer = []


def dfs(depth, idx):
    if len(answer) == M:
        print(" ".join(map(str, answer)))
        return

    for i in range(idx, len(num)):
        answer.append(num[i])
        dfs(depth + 1, i)
        answer.pop()


dfs(0, 0)
