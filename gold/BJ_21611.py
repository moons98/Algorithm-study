# -*- coding: utf-8 -*-
import sys


def blizzard(d, s):
    (x, y) = shark
    for _ in range(s):
        x += dir[d][0]
        y += dir[d][1]
        if 0 > x or x >= N or 0 > y or y >= N:
            break
        else:
            map_lst[x][y] = 0

    return


def snail_loc():
    loc = []
    idx, rep = 0, 1
    (nx, ny) = shark
    while True:
        for _ in range(2):
            for _ in range(rep):
                nx += dir[idx][0]
                ny += dir[idx][1]
                if 0 > nx or nx >= N or 0 > ny or ny >= N:
                    return loc

                loc.append((nx, ny))
            idx = (idx + 1) % 4
        rep += 1

    return


def check_num():
    num = []
    tmp_num, rep = 0, 1
    for x, y in loc:
        val = map_lst[x][y]
        if val == 0:
            continue
        elif val == tmp_num:
            rep += 1
        else:
            num.append([tmp_num, rep])
            tmp_num = val
            rep = 1
    num.append([tmp_num, rep])

    # 처음 0 제거
    num.pop(0)

    return num


def fill_blank(num):
    global map_lst

    new_map = [[0 for _ in range(N)] for _ in range(N)]
    idx = 0
    for val, rep in num:
        for i in range(rep):
            (x, y) = loc[idx]
            new_map[x][y] = val
            idx += 1

    map_lst = new_map

    return


def bead_bomb():
    global map_lst, answer

    while True:
        num = check_num()
        # 4번 이상 중복 시 폭발
        flag = False
        for idx, [val, rep] in enumerate(num):
            if rep >= 4:
                answer[val - 1] += rep
                num.pop(idx)
                flag = True
        # 채우기
        if flag:
            fill_blank(num)
        else:
            break

    return


def group_bead():
    global map_lst

    num = check_num()
    new_num = []
    for i, j in num:
        new_num.append(j)
        new_num.append(i)

    new_map = [[0 for _ in range(N)] for _ in range(N)]
    idx = 0
    for val in new_num[: len(loc)]:
        (x, y) = loc[idx]
        new_map[x][y] = val
        idx += 1

    map_lst = new_map

    return


N, M = map(int, sys.stdin.readline().split())
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

dir = [(0, -1), (1, 0), (0, 1), (-1, 0)]
trans_dir = [3, 1, 0, 2]
shark = (N // 2, N // 2)

magic = []
for _ in range(M):
    td, ts = map(int, sys.stdin.readline().split())
    td = trans_dir[td - 1]
    magic.append((td, ts))

loc = snail_loc()

answer = [0, 0, 0]
for d, s in magic:
    blizzard(d, s)
    fill_blank(check_num())
    bead_bomb()
    group_bead()

print(1 * answer[0] + 2 * answer[1] + 3 * answer[2])

"""
1. 블리자드 마법을 시전 (방향, 거리 안의 얼음 모조리 제거)
2. 빈칸 채우기
3. 구슬 폭발(4개 이상 연속하는 구슬, 빈칸 채우고 반복)
4. 구슬 그룹짓기 + (갯수 번호) 쌍으로 다시 채우기

check_num() 함수에서 제일 마지막 숫자를 append 안하는 실수
"""
