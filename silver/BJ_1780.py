# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())

paper = []
for i in range(N):
    line = list(map(int, sys.stdin.readline().split()))
    paper.append(line)

answer = [0, 0, 0]


def cut_paper(N, x, y):
    num = paper[x][y]

    if N == 1 or all(j == num for i in paper[x : x + N] for j in i[y : y + N]):
        answer[num + 1] += 1
    else:
        N //= 3
        for i in range(3):
            for j in range(3):
                cut_paper(N, x + i * N, y + j * N)


cut_paper(N, 0, 0)
for i in answer:
    print(i)
