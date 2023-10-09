# -*- coding: utf-8 -*-
import math
import sys


def dfs(arr, d):
    global result_max, result_min
    """
    중복 원소가 있을 경우의 순열을 만들어야 함
    """
    if d == len(operator):
        result = num[0]
        for i in range(d):
            if arr[i] == 0:
                result += num[i + 1]
            elif arr[i] == 1:
                result -= num[i + 1]
            elif arr[i] == 2:
                result *= num[i + 1]
            elif arr[i] == 3:
                if result < 0:
                    result = -(-result // num[i + 1])
                else:
                    result //= num[i + 1]

        if result > result_max:
            result_max = result
        if result < result_min:
            result_min = result

        return

    for idx, val in enumerate(operator):
        if not visited[idx] and (idx == 0 or operator[idx - 1] != operator[idx] or visited[idx - 1]):
            arr.append(val)
            visited[idx] = 1
            dfs(arr, d + 1)

            visited[idx] = 0
            arr.pop()

    return


N = int(sys.stdin.readline())
num = list(map(int, sys.stdin.readline().split()))

tmp = list(map(int, sys.stdin.readline().split()))
operator = []
for idx, val in enumerate(tmp):
    for _ in range(val):
        operator.append(idx)

result_max, result_min = -math.inf, math.inf
visited = [0 for _ in operator]

dfs([], 0)

print(result_max)
print(result_min)
