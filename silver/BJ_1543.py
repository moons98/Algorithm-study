# -*- coding: utf-8 -*-
import sys

total_word = list(map(str, sys.stdin.readline()))
word = list(map(str, sys.stdin.readline()))

total_word.pop()
word.pop()

idx, answer = -1, 0
for i in range(len(total_word) - len(word) + 1):
    if i < idx:
        continue
    elif total_word[i : i + len(word)] == word:
        answer += 1
        idx = i + len(word)

print(answer)
