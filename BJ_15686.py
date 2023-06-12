# -*- coding: utf-8 -*-
import sys
from itertools import combinations


def l1_norm(p_lst, p2):
    distance = abs(p_lst[0][0]-p2[0]) + abs(p_lst[0][1]-p2[1])
    for p1 in p_lst[1:]:
        tmp = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
        distance = min(tmp, distance)
        
    return distance

N,M = map(int, sys.stdin.readline().split())

total_store = []
total_house = []
for i in range(N):
    line = list(map(int, sys.stdin.readline().split()))
    for idx, j in enumerate(line):
        if j==1:
            total_house.append([i,idx])
        elif j==2:
            total_store.append([i,idx])

chicken_comb = combinations(total_store, M)
chicken_distance  = [[l1_norm(i, j) for j in total_house] for i in chicken_comb]
chicken_sum = [sum(i) for i in chicken_distance] 

# print(chicken_distance)
# print(chicken_sum)
print(min(chicken_sum))
