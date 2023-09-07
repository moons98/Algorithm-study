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
        tmp = K // i
        K -= tmp * i
        answer += tmp

    if not K:
        print(answer)
        break

"""
단순히 반복문으로 빼도 될 것 같았는데, 몫 계산 안하면 시간초과 발생
"""
