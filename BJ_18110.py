# -*- coding: utf-8 -*-
import sys


def num_round(num):
    return int(num) + 1 if num - int(num) >= 0.5 else int(num)


if __name__ == "__main__":
    N = int(sys.stdin.readline())
    if not N:
        print(0)
    else:
        num = [int(sys.stdin.readline()) for _ in range(N)]
        num.sort()
        rate = num_round(N * 0.15)

        if rate != 0:
            num = num[rate:-rate]

        cnt = N - 2 * rate
        result = sum(num)
        print(num_round(result / cnt))
