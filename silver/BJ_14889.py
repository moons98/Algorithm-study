# -*- coding: utf-8 -*-
import sys
from itertools import combinations

N = int(sys.stdin.readline())
map_lst = [[0 for _ in range(N + 1)]] + [[0] + list(map(int, sys.stdin.readline().split())) for _ in range(N)]

players = set(i + 1 for i in range(N))
comb = list(combinations(players, N // 2))
comb = comb[: len(comb) // 2]

total_score = sum(sum(i) for i in map_lst)

answer = total_score
for player_lst in comb:
    left_lst = list(players - set(player_lst))

    tmp_sum = 0
    for idx1, val1 in enumerate(player_lst):
        for _, val2 in enumerate(player_lst[idx1 + 1 :]):
            tmp_sum += map_lst[val1][val2]
            tmp_sum += map_lst[val2][val1]

    left_sum = 0
    for idx1, val1 in enumerate(left_lst):
        for _, val2 in enumerate(left_lst[idx1 + 1 :]):
            left_sum += map_lst[val1][val2]
            left_sum += map_lst[val2][val1]

    if abs(left_sum - tmp_sum) <= answer:
        answer = abs(left_sum - tmp_sum)

print(answer)

"""
N명을 절반으로 나눠서 계산하면 나머지는 자동으로 계산됨

lst = [i for i in range(20)]
tmp = len(list(combinations(lst, 10)))

  1 2 3 4 5 6
1 0 1 2 3 4 5
2 1 0 2 3 4 5
3 1 2 0 3 4 5
4 1 2 3 0 4 5
5 1 2 3 4 0 5
6 1 2 3 4 5 0
"""
