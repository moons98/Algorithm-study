# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
num = list(map(int, sys.stdin.readline().split()))

memorization = [0]
for i in num:
    if memorization[-1] < i:
        memorization.append(i)
    else:
        start, end = 0, len(memorization)
        while start <= end:
            mid = (start + end) // 2
            if memorization[mid] < i:
                start = mid + 1
            else:
                end = mid - 1
        memorization[start] = i

print(len(memorization) - 1)


"""
입력 크기가 커서 기존의 이중 for문으로는 해결 불가능
이분 탐색은 해당 인덱스를 찾아 숫자를 바꿔버리는 식으로 동작하는데, 실제로는 불가능한 배열이 나옴 (길이만 같음)
-> 중간의 값을 바꾸면 이후의 값들도 바뀐 값 뒤의 값을 차례로 바꿔나가기 때문에 직관적으로는 dp와 같이 동작한다고도 이해할 수 있음
"""

"""
import sys
from bisect import bisect_left

N = int(sys.stdin.readline())
num = list(map(int, sys.stdin.readline().split()))

memorization = [0]
for i in num:
    if memorization[-1] < i:
        memorization.append(i)
    else:
        target = bisect_left(memorization, i)
        memorization[target] = i

print(len(memorization) - 1)
"""
