# -*- coding: utf-8 -*-
import sys


def move_and_split(map_lst):
    new_lst = [[[] for _ in range(N)] for _ in range(N)]

    # move
    for x, val in enumerate(map_lst):
        for y, val2 in enumerate(val):
            for m, s, d in val2:
                tx = dir[d][0] * s
                ty = dir[d][1] * s

                nx, ny = x + tx, y + ty
                if 0 > nx:
                    nx += -(nx // N) * N
                elif nx >= N:
                    nx -= (nx // N) * N
                if 0 > ny:
                    ny += -(ny // N) * N
                elif ny >= N:
                    ny -= (ny // N) * N

                new_lst[nx][ny].append([m, s, d])

    # split
    for x in range(N):
        for y in range(N):
            if len(new_lst[x][y]) >= 2:
                tmp = [[], [], []]
                for m, s, d in new_lst[x][y]:
                    tmp[0].append(m)
                    tmp[1].append(s)
                    tmp[2].append(d)

                nm = int(sum(tmp[0]) / 5)
                if nm:
                    ns = int(sum(tmp[1]) / len(new_lst[x][y]))
                    dirs = [i % 2 for i in tmp[2]]
                    if all(dirs) == 1 or not any(dirs):
                        nd = [0, 2, 4, 6]
                    else:
                        nd = [1, 3, 5, 7]

                    new_lst[x][y] = [[nm, ns, nd[i]] for i in range(4)]
                else:
                    new_lst[x][y] = []

    return new_lst


N, M, K = map(int, sys.stdin.readline().split())
map_lst = [[[] for _ in range(N)] for _ in range(N)]
dir = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

for i in range(M):
    r, c, m, s, d = map(int, sys.stdin.readline().split())
    map_lst[r - 1][c - 1].append([m, s, d])

for _ in range(K):
    map_lst = move_and_split(map_lst)

# print
answer = 0
for i in range(N):
    for j in range(N):
        for k in map_lst[i][j]:
            answer += k[0]
print(answer)

"""
dictionary 사용해서 fireball을 운용하는 사람도 많음
이 경우에 전체 맵을 순회할 필요 없으므로 시간적 이득 발생
"""
