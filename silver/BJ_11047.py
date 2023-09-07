# -*- coding: utf-8 -*-
import sys

N, K = map(int, sys.stdin.readline().split())

coin = []
for _ in range(N):
    coin.append(int(sys.stdin.readline()))

coin.sort(reverse=True)

answer = 0
for i in coin:
    while K >= i:
        K -= i
        answer += 1

    if not K:
        print(answer)
        break
