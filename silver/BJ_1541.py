# -*- coding: utf-8 -*-
import sys

eq = sys.stdin.readline().strip()

eq_lst = []
start = 0
for idx, val in enumerate(eq):
    if val == "-" or val == "+":
        eq_lst.append(int(eq[start:idx]))
        eq_lst.append(val)
        start = idx + 1
eq_lst.append(int(eq[start:]))

queue = []
tmp = 0
for i in eq_lst[::-1]:
    if i == "-":
        queue.append(-tmp)
        tmp = 0
    elif i == "+":
        continue
    else:
        tmp += i

print(tmp + sum(queue))

"""
- 나오면 다음 - 나올때까지 다 더하기, queue 활용해서 구현
저장하는 idx 문제로 30-40+20-1 에서 마지막 숫자 잘리는 문제 발생
"""
