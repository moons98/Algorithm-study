# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())

dp = [0 for _ in range(N + 1)]
for i in range(2, N + 1):
    dp[i] = dp[i - 1] + 1
    if i % 3 == 0:
        dp[i] = min(dp[i], dp[i // 3] + 1)
    if i % 2 == 0:
        dp[i] = min(dp[i], dp[i // 2] + 1)
print(dp[-1])

"""
연산의 우선순위를 두고 풀면 시간초과 발생
dp로 접근

%2, %3 연산을 if와 elif로 연결했는데, 이러면 틀리는 예가 있나봄
"""
