# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
num = list(map(int, sys.stdin.readline().split()))
rev_num = num[::-1]

ori_dp = [1 for _ in range(N)]
rev_dp = [1 for _ in range(N)]
for i in range(N):
    for j in range(i):
        if num[i] > num[j]:
            ori_dp[i] = max(ori_dp[j] + 1, ori_dp[i])
        if rev_num[i] > rev_num[j]:
            rev_dp[i] = max(rev_dp[j] + 1, rev_dp[i])

sum_dp = [i + j for i, j in zip(ori_dp, rev_dp[::-1])]
print(max(sum_dp) - 1)

"""
마찬가지로 시간 제한이 넉넉해서 N^2으로 풀이 가능
"""
