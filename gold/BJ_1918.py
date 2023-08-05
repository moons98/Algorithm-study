# -*- coding: utf-8 -*-
import sys

infix = sys.stdin.readline().rstrip()
priority = {"(": 1, ")": 1, "+": 2, "-": 2, "*": 3, "/": 3}

operator_stack = []
answer = []
for i in infix:
    if i == "(":
        operator_stack.append(i)
    elif i == ")":
        while operator_stack[-1] != "(":
            op = operator_stack.pop()
            answer.append(op)
        operator_stack.pop()  # '(' 삭제를 위함
    elif i in ["+", "-", "*", "/", "(", ")"]:
        try:
            while priority[i] <= priority[operator_stack[-1]]:
                op = operator_stack.pop()
                answer.append(op)
            operator_stack.append(i)
        except:
            operator_stack.append(i)
    else:
        answer.append(i)

# 남은 연산자들 붙이기
for i in operator_stack[::-1]:
    answer.append(i)

print("".join(answer))
