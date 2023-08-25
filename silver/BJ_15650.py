# -*- coding: utf-8 -*-
import sys

N, M = map(int, sys.stdin.readline().split())

answer = []


def dfs(depth, idx):
    if len(answer) == M:
        print(" ".join(map(str, answer)))
        return

    for i in range(idx, N + 1):
        answer.append(i)
        dfs(depth + 1, i + 1)
        answer.pop()


dfs(0, 1)
