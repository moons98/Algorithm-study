# -*- coding: utf-8 -*- 
import sys

N = int(sys.stdin.readline())
num_lst = list(map(int, sys.stdin.readline().split()))
K = int(sys.stdin.readline())

start = 0
end = 0
total_sum = num_lst[0]

answer = 0
for idx, _ in enumerate(num_lst):
    while total_sum<=K and end<len(num_lst)-1:
        end += 1
        total_sum += num_lst[end]
    if total_sum <= K:
        break
    else:
        answer += len(num_lst) - end
        total_sum -= num_lst[start]
        start += 1

print(answer)
