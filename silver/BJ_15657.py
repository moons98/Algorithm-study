# -*- coding: utf-8 -*-
import sys

N, M = map(int, sys.stdin.readline().split())
num = sorted(list(map(int, sys.stdin.readline().split())))
answer = []


def dfs(depth, idx):
    if depth == M:
        print(" ".join(map(str, answer)))
        return

    for i in range(idx, N):
        answer.append(num[i])
        dfs(depth + 1, i)
        answer.pop()


dfs(0, 0)

"""
back-tracking (퇴각검색)
한정조건 내에서 모든 경우의 수를 탐색하는 것
한정 조건을 만족하는 경우를 탐색하는 것이기 때문에 완전탐색기법인 BFS와 DFS 사용 가능

depth는 문자열의 길이, idx는 문자열의 수를 의미
따라서 depth가 깊어질수록 앞에서 사용한 문자열 이상의 값들을 하나씩 채우게 함
"""
