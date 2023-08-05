# -*- coding: utf-8 -*- 

# 첫 번째 자리는 2개만 가능, 마지막 자리는 고정됨 -> 즉 2* 3**(N-2)으로 풀이 가능
ans = 2 * int(3 ** (int(input()) - 2))
ans %= (10**9+9)
print(ans)
