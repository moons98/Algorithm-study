# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
card = list(map(int, sys.stdin.readline().split()))

option = [sum(card[::2]), sum(card[1:][::2])]
answer = max(option)
score = [0, 0, *option]
for i in range(0, N, 2):
    score[0] += card[i]
    score[2] -= card[i]

    tmp = score.copy()
    if tmp[2] != 0:
        tmp[1] += card[-1]
        tmp[3] -= card[-1]
        if tmp[0] + tmp[3] > answer:
            answer = tmp[0] + tmp[3]

    score[1] += card[i + 1]
    score[3] -= card[i + 1]

    if score[0] + score[3] > answer:
        answer = score[0] + score[3]

print(answer)

"""
4
100 50 10 2
out:150

[0 100 110] [0 50 52]


2
100 70
out:100
"""
