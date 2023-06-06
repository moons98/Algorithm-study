# -*- coding: utf-8 -*- 
import sys
from itertools import permutations

N, M = map(int, sys.stdin.readline().split())
num = map(int, sys.stdin.readline().split())

perm = permutations(num, M)
sorted_perm = sorted(set([i for i in perm]))

for i in sorted_perm:
    print(' '.join(map(str, i)))
    # print(f"{i[0]}, {i[1]}") # 왜 에러나지?
    