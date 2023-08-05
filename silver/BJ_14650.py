# -*- coding: utf-8 -*- 
import sys
from itertools import product

num = int(sys.stdin.readline())
cases = product(['0', '1', '2'], repeat=num)

# 0으로 시작하지 않고, 3의 배수인 수의 총 갯수
print(len([case for case in cases if case[0] != '0' and int(''.join(case)) % 3 == 0]))