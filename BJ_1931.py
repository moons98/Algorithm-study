# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())

meeting = []
for _ in range(N):
    start, end = map(int, sys.stdin.readline().split())
    meeting.append([start, end])

meeting.sort(key=lambda x: (x[1], x[0]))

cnt = 0
end_time = 0
for start, end in meeting:
    if start >= end_time:
        cnt += 1
        end_time = end

print(cnt)

"""
단순히 종료 시간, 시작 시간으로 정렬하고 그리디로 접근하면 optimal answer를 낸다는 게 잘 이해가 가지 않음
"""
