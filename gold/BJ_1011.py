# -*- coding: utf-8 -*- 
import sys
import math

'''
제곱수를 기준으로, 커질 때마다 trial이 하나씩 증가
제곱근 + 제곱수에서 trial 한 번 더 증가

'''

num = int(input())
lst = []
for _ in range(num):
    x,y = map(int, sys.stdin.readline().split())
    x_new, y_new = 0, y-x

    trial = 0
    digit = 1
    square_num = int(math.floor(math.sqrt(y_new))) # 가장 가까운, 작은 제곱수 찾기
    
    y_new -= square_num**2
    trial += (2*square_num -1)
    
    # 제곱수면 return
    if y_new == 0:
        pass
    # 만약 square_num보다 작은 값이 남았으면
    elif y_new <= square_num:
        trial += 1
    # 제곱근+제곱수에서 한 번 값이 더 바뀜 (ex. 4+2, 9+3, 16+4 ...)
    else:
        trial += 2        
    
    lst.append(trial)
    
for i in lst:
    print(i)
