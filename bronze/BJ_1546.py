# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())

score = list(map(float, sys.stdin.readline().split()))
new_mean = sum(score) / max(score) * 100 / N
print(new_mean)
