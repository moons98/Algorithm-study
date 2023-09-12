# -*- coding: utf-8 -*-
import sys

n = int(sys.stdin.readline())

dp = [0, 1, 3, 5] + [0 for _ in range(997)]
for i in range(1001):
    if i >= 4:
        dp[i] = dp[i - 2] * 2 + dp[i - 1]

print(dp[n] % 10007)

"""
a: 2x1, b: 2x2, c: 1x2

2x1 : a -> 1

2x2 : aa, b, c -> 3

2x3 : aaa, (ab)x2, (ac)x2 -> 5

2x4 : aaaa, (aab)x3, (aac)x3, (bc)x2, bb, cc -> 11

2x5 : aaaaa, (aaab)x4, (aaac)x4, (abb)x3, (acc)x3, (abc)x6 -> 21

2x6 : aaaaaa, (aaaab)x5, (aaaac)x5, (aabb)x6, (aacc)x6, (aabc)x12, (bbc)x3, (bcc)x3, 
    bbb, ccc -> 43

점화식이 어떤 의미에서 생기는 지 생각해볼 것
x[n] = x[n-2]*2 + x[n-1]
"""
