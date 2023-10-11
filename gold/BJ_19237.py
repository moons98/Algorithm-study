# -*- coding: utf-8 -*-
import sys


def find_loc(num):
    for x in range(N):
        for y in range(N):
            if map_lst[x][y] and map_lst[x][y][0] == num:
                return x, y, map_lst[x][y][1]

    return False


def move_shark(map_lst):
    global M, answer

    for i in range(1, M + 1):
        if find_loc(i):
            x, y, d = find_loc(i)

            # 움직일 수 있는 좌표를 우선순위 순서대로 따라가서 확인
            available_loc = [[] for _ in range(2)]
            for j in range(4):
                # 우선순위 0번부터 탐색
                idx = priority[i - 1][d][j]
                nx = x + loc[idx][0]
                ny = y + loc[idx][1]
                if 0 > nx or nx >= N or 0 > ny or ny >= N:
                    continue
                # 아무 냄새가 없는 좌표
                elif not smell_map[nx][ny] or smell_map[nx][ny][1] < answer:
                    available_loc[0].append([nx, ny, idx])
                    break
                # 자신의 냄새
                elif smell_map[nx][ny][0] == i and smell_map[nx][ny][1] >= answer:
                    available_loc[1].append([nx, ny, idx])

            if available_loc[0]:
                nx, ny, idx = available_loc[0][0]
            else:
                nx, ny, idx = available_loc[1][0]

            # 움직이기, 작은 번호로 대체
            map_lst[x][y] = [0, 0]
            if map_lst[nx][ny][0] == 0:
                map_lst[nx][ny] = [i, idx]
            elif i < map_lst[nx][ny][0]:
                map_lst[nx][ny] = [i, idx]

    return


def add_smell(map_lst):
    num_shark = 0
    # 냄새 추가
    for x in range(N):
        for y in range(N):
            if map_lst[x][y][0] != 0:
                smell_map[x][y] = [map_lst[x][y][0], answer + K]

                num_shark += 1

    return True if num_shark == 1 else False


N, M, K = map(int, sys.stdin.readline().split())

shark = {}
for x in range(N):
    tmp = list(map(int, sys.stdin.readline().split()))
    for y, val in enumerate(tmp):
        if val != 0:
            shark[val] = [x, y]

# 상어 번호, 방향
map_lst = [[[0, 0] for _ in range(N)] for _ in range(N)]
smell_map = [[[] for _ in range(N)] for _ in range(N)]
for val, d in enumerate(list(map(int, sys.stdin.readline().split()))):
    [x, y] = shark[val + 1]
    map_lst[x][y] = [val + 1, d - 1]
    smell_map[x][y] = [val + 1, K]


priority = [[[i - 1 for i in list(map(int, sys.stdin.readline().split()))] for _ in range(4)] for _ in range(M)]
loc = [(-1, 0), (1, 0), (0, -1), (0, 1)]

answer = 0
while True:
    answer += 1
    move_shark(map_lst)

    flag = add_smell(map_lst)
    if flag:
        break
    if answer == 1000:
        answer = -1
        break


print(answer)

"""
11:26 ~ 02:02 (2시간 반 소요)

다른 상어가 냄새 뿌리면 그 냄새만 남음
자기 냄새는 '남고', 남의 냄새는 '지나간' 조건을 잘못 맞춰줌
"""
