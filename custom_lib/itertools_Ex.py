# -*- coding: utf-8 -*-
import sys
from itertools import combinations, permutations


def dfs_comb(lst, d, all_lst, tmp_lst, tn, visited):
    if d == tn:
        # 항상 결과 저장에는 깊은 복사를 해주어야 함!!
        all_lst.append(lst[:])
        return

    start = tmp_lst.index(lst[-1]) + 1 if lst else 0
    for i in range(start, len(tmp_lst)):
        # 중복 원소의 처리
        if i == 0 or tmp_lst[i - 1] != tmp_lst[i] or visited[i - 1]:
            lst.append(tmp_lst[i])
            visited[i] = 1
            dfs_comb(lst, d + 1, all_lst, tmp_lst, tn, visited)

            lst.pop()
            visited[i] = 0

    return


def custom_combination(tmp_lst, tn):
    """
    순서에 상관없으므로 뒤의 숫자만을 dfs로 돌림
    """
    tmp_lst.sort()
    visited = [0 for _ in tmp_lst]

    lst = []
    all_lst = []
    dfs_comb(lst, 0, all_lst, tmp_lst, tn, visited)

    return all_lst


###
def dfs_perm(lst, d, all_lst, tmp_lst, tn, visited):
    if d == tn:
        all_lst.append(lst[:])
        return

    for i in range(len(tmp_lst)):
        # 중복 처리
        if not visited[i] and (i == 0 or tmp_lst[i - 1] != tmp_lst[i] or visited[i - 1]):
            lst.append(tmp_lst[i])
            visited[i] = 1
            dfs_perm(lst, d + 1, all_lst, tmp_lst, tn, visited)

            lst.pop()
            visited[i] = 0

    return


def custom_permutation(tmp_lst, tn):
    """
    자기 자신만 빼고 앞에서부터 중복 돌아야 함
    """
    all_lst, lst = [], []
    visited = [0 for _ in tmp_lst]
    dfs_perm(lst, 0, all_lst, tmp_lst, tn, visited)

    return all_lst


num_lst = [1, 1, 2, 3, 4, 5]
n = 3


result = list(combinations(num_lst, 2))  # 중복이 일어나도 그냥 조합을 돌려버림
print(result)

print()
result_comb = custom_combination(num_lst, 2)
print(result_comb)

print()
result = list(permutations(num_lst, 2))  # 중복이 일어나도 그냥 조합을 돌려버림
print(result)

print()
result_perm = custom_permutation(num_lst, 2)
print(result_perm)

"""
중복된 원소에 대한 처리까지 더해서 back-tracking으로 구현
https://shoark7.github.io/programming/algorithm/Permutations-and-Combinations
"""
