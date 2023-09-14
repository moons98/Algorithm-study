# -*- coding: utf-8 -*-
import sys

N, S = map(int, sys.stdin.readline().split())
num = list(map(int, sys.stdin.readline().split()))

dp = [0, num[0]]
for i in range(1, N):
    dp.append(dp[i] + num[i])

answer = N + 1
tmp = 0
for idx1, val1 in enumerate(dp):
    if val1 < S:
        continue
    elif dp[idx1] - dp[idx1 - 1] == S:
        answer = 1
        break
    else:
        for idx2 in range(tmp, idx1 + 1):
            if val1 - dp[idx2] < S:
                answer = min(answer, idx1 - idx2 + 1)
                tmp = idx2 - 1
                break

if answer == N + 1:
    print(0)
else:
    print(answer)

"""
첫 숫자가 S보다 클 때, 특정 숫자가 S와 같은 값을 가지는 경우를 한번에 처리하지 못함

10 15
16 1 3 5 10 7 4 9 2 8

10 10
10 1 1 1 1 1 1 1 1 1
"""
