# -*- coding: utf-8 -*-
import sys


def check_word(word):
    stack = []
    for i in word:
        if i == "(" or i == "[":
            stack.append(i)
        elif i == ")":
            if not stack:
                return "no"
            elif stack[-1] == "(":
                stack.pop()
            else:
                return "no"
        elif i == "]":
            if not stack:
                return "no"
            elif stack[-1] == "[":
                stack.pop()
            else:
                return "no"

    if stack:
        return "no"
    else:
        return "yes"


answer = []
while True:
    word_lst = list(map(str, sys.stdin.readline().rstrip()))
    if word_lst == ["."]:
        break

    answer.append(check_word(word_lst))

for i in answer:
    print(i)

"""
생각보다 조건문을 잘 생각하고 달아야 함
안되는 경우를 놓치고 루프 안끊기는 경우가 있어 실패를 많이 함
"""
