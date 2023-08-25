# -*- coding: utf-8 -*-
import sys
from collections import Counter

tmp = sys.stdin.readline().rstrip()
word = [i.lower() for i in tmp]

word_cnt = Counter(word)
max_value = max(word_cnt.values())

answer = []
for key in word_cnt.keys():
    if word_cnt[key] == max_value:
        answer.append(key)

if len(answer) != 1:
    print("?")
else:
    print(answer[-1].upper())
