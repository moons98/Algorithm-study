# -*- coding: utf-8 -*-
import sys

point = []
for _ in range(3):
    x,y = map(int, sys.stdin.readline().split())
    point.append([x,y])

vec = [[point[i][0]-point[i+1][0], point[i][1]-point[i+1][1]] for i in range(2)]

cross = vec[0][0]*vec[1][1] - vec[0][1]*vec[1][0]
if cross > 0:
    print(1)
elif cross < 0:
    print(-1)
else:
    print(0)
