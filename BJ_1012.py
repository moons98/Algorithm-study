# -*- coding: utf-8 -*- 
import sys
from collections import deque

# BFS, queue, 최단경로
# 미완 -> RunTimeError
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]
def BFS(place, loc):
    bundle = 0
    queue = deque()
    # for i in place:
        # print(i)
    for loc_y, loc_x in loc:
        if place[loc_y][loc_x] ==1:
            # print(loc_y, loc_x)
            queue.append([loc_y, loc_x])
            while queue:
                y, x = queue.popleft()
                place[y][x] += 1
                for i in range(4):
                    nx = x + dx[i]
                    ny = y + dy[i]
                    if 0<=nx<=M-1 and 0<=ny<=N-1 and place[ny][nx]==1:
                        queue.append([ny, nx])    
            bundle += 1
        else:
            continue
        
    return bundle
    

# Main
num_case = input()
ans_lst = []
for i in range(num_case):
    M, N, K = map(int, sys.stdin.readline().split())
    place = [[0 for m in range(M)] for n in range(N)] # 0부터 index가 시작함
    
    loc = list()
    for j in range(K):
        x, y = map(int, sys.stdin.readline().split())
        loc.append([y,x])
        place[y][x] = 1
    
    answer = BFS(place, loc)
    ans_lst.append(answer)
    
for i in ans_lst:
    print(i)
