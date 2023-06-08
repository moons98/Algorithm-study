# -*- coding: utf-8 -*- 
import sys

N = int(sys.stdin.readline())
last = [1 for i in range(10)]

for i in range(N-1):
    for j in range(1,10):
        last[j] += last[j-1]
    print(last)

print(sum(last)%10007)
