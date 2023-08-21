# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())

answer = N
last_word = None
for i in range(N):
    word = sys.stdin.readline().rstrip()
    word_set = set()
    for w in word:
        if w not in word_set:
            word_set.add(w)
        elif last_word == w:
            continue
        else:
            answer -= 1
            break
        last_word = w

print(answer)
