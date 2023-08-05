# -*- coding: utf-8 -*-
import sys
from collections import deque

N, M, A, B = map(int, sys.stdin.readline().split())

bin = set()
for i in range(M):
    L, R = map(int, sys.stdin.readline().split())
    num_range = [j for j in range(L, R + 1)]
    bin.update(num_range)

num_lst = [A, B]


def dfs():
    queue = deque([[0, 0]])  # 총 강아지 수, 횟수
    visit = set()  # 한 번 방문한 숫자는 방문할 필요 없음, 시간초과 방지
    while queue:
        total, answer = queue.popleft()
        for i in range(2):
            tmp_total = total + num_lst[i]
            if tmp_total not in bin and tmp_total < N and tmp_total not in visit:
                queue.append([tmp_total, answer + 1])
                visit.add(tmp_total)
            elif tmp_total == N:
                return answer + 1

    return -1


answer = dfs()
print(answer)
