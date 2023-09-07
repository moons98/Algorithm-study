# -*- coding: utf-8 -*-
import sys

word = []
for _ in range(2):
    tmp = sys.stdin.readline().rstrip()
    word.append(["0"] + [str(i) for i in tmp])

dp = [[0 for _ in range(len(word[1]))] for _ in range(len(word[0]))]
for idx1, val1 in enumerate(word[0]):
    for idx2, val2 in enumerate(word[1]):
        if idx1 == 0 or idx2 == 0:
            continue
        if val1 == val2:
            dp[idx1][idx2] = dp[idx1 - 1][idx2 - 1] + 1
        else:
            dp[idx1][idx2] = max(dp[idx1 - 1][idx2], dp[idx1][idx2 - 1])

print(dp[-1][-1])

"""
2차원 배열로 접근해야 함, 아래 링크 참조 (+문자열을 거슬러 올라가면서 찾는 방법도 있음)
https://velog.io/@emplam27/%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EA%B7%B8%EB%A6%BC%EC%9C%BC%EB%A1%9C-%EC%95%8C%EC%95%84%EB%B3%B4%EB%8A%94-LCS-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-Longest-Common-Substring%EC%99%80-Longest-Common-Subsequence
"""
