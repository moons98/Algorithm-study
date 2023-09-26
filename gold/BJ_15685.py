# -*- coding: utf-8 -*-
import sys


def dragon_curve(map_lst, x, y, d, g):
    dir = [d]
    nx, ny = y, x
    map_lst[nx][ny] = 1

    nx += dx[d]
    ny += dy[d]
    map_lst[nx][ny] = 1

    for _ in range(g):
        new_dir = []
        for i in dir:
            new_dir.append((i + 1) % 4)

        for j in new_dir[::-1]:
            nx += dx[j]
            ny += dy[j]
            if 0 <= nx <= 100 and 0 <= ny <= 100:
                map_lst[nx][ny] = 1

            dir.append(j)

    return map_lst


map_lst = [[0 for _ in range(101)] for _ in range(101)]

dx = [0, -1, 0, 1]
dy = [1, 0, -1, 0]

N = int(sys.stdin.readline())
for _ in range(N):
    x, y, d, g = map(int, sys.stdin.readline().split())
    map_lst = dragon_curve(map_lst, x, y, d, g)

answer = 0
for i in range(100):
    for j in range(100):
        if map_lst[i][j] == 1 and map_lst[i + 1][j] == 1 and map_lst[i][j + 1] == 1 and map_lst[i + 1][j + 1] == 1:
            answer += 1

print(answer)

# for i in map_lst[:30]:
#     print(i[:30])

"""
방향이 0 -> 0 + 1 -> 0,1 + 2,1 -> 0,1,2,1 + 2,3,2,1
기존까지의 방향의 +1 하고, 순서를 반대로 붙이는 방식 

문제에 100x100이라길래 0~99 index 가지게 설정했는데, 실제 조건에는 0~100까지 index 가져서 틀림
"""
