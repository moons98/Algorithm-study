# -*- coding: utf-8 -*-
import sys
from collections import Counter

"""
3x3 행렬 A, idx는 1부터 시작
    - R 연산 : 모든 행에 대해서 정렬 수행 (행 >= 열의 갯수일 때 적용)
    - C 연산 : 모든 열에 대해서 정렬 수행 (열 >> 행의 갯수일 때 적용)
    
정렬 : 수의 등장 횟수가 커지는 순 >> 수가 커지는 순
    - 수, 등장횟수, 수, 등장횟수 ,,,
    - 정렬 후에는 가장 큰 행 // 열 기준으로 크기가 변함
    - 커진 곳에는 0이 채워짐, 수 정렬에서 0은 무시
    - 100을 넘어가면 처음 100개만 유지

A[r][c] == k 되기 위한 최소 시간, 100초 지나면 -1 출력
"""


def print_map(a):
    for i in a:
        print(i)
    print()


r, c, k = map(int, sys.stdin.readline().split())

arr = [list(map(int, sys.stdin.readline().split())) for _ in range(3)]


time = 0
while True:
    nr, nc = len(arr), len(arr[0])

    if nr >= r and nc >= c and arr[r - 1][c - 1] == k:
        print(time)
        break
    elif time == 100:
        print(-1)
        break

    new_arr = []
    size_max = 0

    if nr >= nc:
        for i in range(nr):
            arr_counter = Counter(arr[i])

            # 0이 있는 경우 삭제
            if 0 in arr_counter.keys():
                del arr_counter[0]

            # 정렬
            arr_item = list(arr_counter.items())
            arr_item.sort(key=lambda x: (x[1], x[0]))

            # size 갱신
            size_max = max(size_max, len(arr_item) * 2)
            new_arr.append(arr_item)

        # size 기반으로 0 채우기, 100 이상이면 100개만 유지
        if size_max > 100:
            size_max = 100

        # arr 덮어쓰기
        arr = [[0 for _ in range(size_max)] for _ in range(nr)]

        for i in range(nr):
            for idx, (val, rep) in enumerate(new_arr[i]):
                arr[i][2 * idx : 2 * (idx + 1)] = [val, rep]

                if idx == 50:
                    break

    else:
        for i in range(nc):
            tmp = []
            arr_counter = Counter([col[i] for col in arr])

            # 0이 있는 경우 삭제
            if 0 in arr_counter.keys():
                del arr_counter[0]

            # 정렬
            arr_item = list(arr_counter.items())
            arr_item.sort(key=lambda x: (x[1], x[0]))

            # size 갱신
            size_max = max(size_max, len(arr_item) * 2)
            new_arr.append(arr_item)

        # size 기반으로 0 채우기, 100 이상이면 100개만 유지
        if size_max > 100:
            size_max = 100

        # arr 덮어쓰기
        arr = [[0 for _ in range(nc)] for _ in range(size_max)]
        for i in range(nc):
            for idx, (val, rep) in enumerate(new_arr[i]):
                arr[2 * idx][i] = val
                arr[2 * idx + 1][i] = rep

                if idx == 50:
                    break

    time += 1
