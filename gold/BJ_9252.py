# -*- coding: utf-8 -*-
import sys

word = []
for _ in range(2):
    tmp = sys.stdin.readline().strip()
    word.append([0] + list(i for i in tmp))

dp = [[0 for _ in word[1]] for _ in word[0]]
for idx1, val1 in enumerate(word[0]):
    for idx2, val2 in enumerate(word[1]):
        if idx1 == 0 or idx2 == 0:
            continue
        if val1 == val2:
            dp[idx1][idx2] = dp[idx1 - 1][idx2 - 1] + 1
        else:
            dp[idx1][idx2] = max(dp[idx1 - 1][idx2], dp[idx1][idx2 - 1])

find_word = []
x, y = len(dp) - 1, len(dp[0]) - 1
while x > 0 and y > 0:
    if dp[x][y] == dp[x - 1][y]:
        x -= 1
    elif dp[x][y] == dp[x][y - 1]:
        y -= 1
    else:
        find_word.append(word[0][x])
        x -= 1
        y -= 1

print(dp[-1][-1])
if find_word:
    print("".join(find_word[::-1]))

"""
ACAYKP
CAPCAK

    C A P C A K
  0 0 0 0 0 0 0
A 0 0 1 1 1 1 1
C 0 1 1 1 2 2 2
A 0 1 2 2 2 3 3
Y 0 1 2 2 2 3 3
K 0 1 2 2 2 3 4
P 0 1 2 3 3 3 4

공통 부분이 없으면 출력하지 않도록
ASDF
QWER

두 문자열의 길이가 달라도 출력 가능하도록 (x, y = len(dp) - 1, len(dp[0]) - 1)
AAA
XX
"""
