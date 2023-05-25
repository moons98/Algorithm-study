# -*- coding: utf-8 -*- 
import sys

answer = 0
num_building = int(input())
building = list(map(int, sys.stdin.readline().split()))

for idx, val in enumerate(building):
    std = [building[i] - building[idx] for i in range(num_building)]
    #print(tmp)
    slope = 