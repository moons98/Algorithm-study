# -*- coding: utf-8 -*-
import sys

A, B, C = map(int, sys.stdin.readline().split())


def power(a, b):
    if b == 1:
        return a % C
    else:
        tmp = power(a, b // 2)
        if b % 2 == 0:
            return (tmp * tmp) % C
        else:
            return (tmp * tmp * a) % C


print(power(A, B))

"""
10 11 12

power(10, 11) -> tmp = power(10, 5), return tmp*tmp *10 %C 
power(10, 5)  -> tmp = power(10, 2), return tmp*tmp *10 %C
power(10, 2)  -> tmp = power(10, 1), return tmp*tmp %C
power(10, 1)  ->                     return 10

일반 거듭제곱은 O(N)의 복잡도를 가지지만, 분할정복을 통하면 O(logN)의 복잡도를 가짐
"""
