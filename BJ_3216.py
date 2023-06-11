# -*- coding: utf-8 -*-
import sys
from collections import deque

N = int(sys.stdin.readline())

play_sum = 0
down_sum = 0
l = []
ans = 0
for i in range(N):
    a, b = map(int, input().split())
    l.append([a, b])
    play_sum += a
    down_sum += b
    ans = max(ans, down_sum - (play_sum - a))

print(ans)

"""
이번 것까지 다운로드 하는데 걸리는 시간 - (이번 조각 전까지 플레이 타임)
-> 구간 별로 최소 안끊기기 위해 필요한 시간 중 가장 큰 값이 정답
"""
