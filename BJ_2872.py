# -*- coding: utf-8 -*- 
import sys

N = int(sys.stdin.readline())

lst = []
for i in range(N):
    num = int(sys.stdin.readline())
    lst.append(num)

# 제일 큰 수 기준으로 하나씩 작아지는 수들은 다시 뺄 필요가 없음
bottom = lst.index(N)
answer = N-1
max_book = N
for i in lst[:bottom][::-1]:
    if i == max_book-1:
        answer -= 1
        max_book = i
        
print(answer)