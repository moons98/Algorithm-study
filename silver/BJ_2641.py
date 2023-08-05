# -*- coding: utf-8 -*-
import sys


def tf_pt(i):
    i = int(i)
    if i <= 2:
        return str(i + 2)
    else:
        return str(i - 2)


def check_std(std, rev_std, tmp):
    if tmp in std * 2:
        return True
    elif tmp in rev_std[::-1] * 2:
        return True
    else:
        return False


length = int(sys.stdin.readline())
std = "".join(map(str, sys.stdin.readline().split()))
rev_std = "".join([tf_pt(i) for i in std])

num = int(sys.stdin.readline())
num_lst = []
for i in range(num):
    tmp = sys.stdin.readline().rstrip()
    tmp_str = "".join(list(map(str, tmp.split())))
    if check_std(std, rev_std, tmp_str):
        num_lst.append(tmp)

print(len(num_lst))
for i in num_lst:
    print(i)

# def check_std(std, rev_std, tmp):
#     if tmp in std * 2 or tmp in std[::-1] * 2:
#         return True
#     elif tmp in rev_std * 2 or tmp in rev_std[::-1] * 2:
#         return True
#     else:
#         return False
