# -*- coding: utf-8 -*-
import sys


def girl_switch(num):
    idx = 0
    while True:
        if num - idx <= 0 or num + idx > N:
            idx -= 1
            break
        elif switch[num - idx] != switch[num + idx]:
            idx -= 1
            break
        else:
            idx += 1

    for i in range(num - idx, num + idx + 1):
        switch[i] = 1 - switch[i]

    return


def boy_switch(num):
    for i in range(1, int(N // num) + 1):
        switch[i * num] = 1 - switch[i * num]

    return


N = int(sys.stdin.readline())
switch = [0] + list(map(int, sys.stdin.readline().split()))

num_people = int(sys.stdin.readline())
order = [list(map(int, sys.stdin.readline().split())) for _ in range(num_people)]

for gender, num in order:
    if gender == 1:
        boy_switch(num)
    elif gender == 2:
        girl_switch(num)

rep = int(N // 20) + 1
for i in range(rep):
    if i == rep:
        print(*switch[i * 20 + 1 :], sep=" ")
    else:
        print(*switch[i * 20 + 1 : (i + 1) * 20 + 1], sep=" ")


"""
8
0 1 0 1 0 0 0 1
5
2 2
2 3
2 4
2 5
2 6
"""
