# -*- coding: utf-8 -*-
import sys


def roll_dice(dice, direction):
    # [상,하,동,서,남,북] 순서
    if direction == 1:  # 서,동,상,하,남,북
        new_dice = [dice[3], dice[2], dice[0], dice[1], dice[4], dice[5]]
    elif direction == 2:  # 동,서,하,상,남,북
        new_dice = [dice[2], dice[3], dice[1], dice[0], dice[4], dice[5]]
    elif direction == 3:  # 남,북,동,서,하,상
        new_dice = [dice[4], dice[5], dice[2], dice[3], dice[1], dice[0]]
    elif direction == 4:  # 북,남,동,서,상,하
        new_dice = [dice[5], dice[4], dice[2], dice[3], dice[0], dice[1]]

    return new_dice


N, M, x, y, K = map(int, sys.stdin.readline().split())
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

dx = [0, 0, -1, 1]
dy = [1, -1, 0, 0]

dice = [0, 0, 0, 0, 0, 0]
answer = []

# 동서북남 = 1234 -> 0123으로 변환
order = list(map(int, sys.stdin.readline().split()))
for i in order:
    nx = x + dx[i - 1]
    ny = y + dy[i - 1]
    if 0 <= nx < N and 0 <= ny < M:
        dice = roll_dice(dice, i)
        if map_lst[nx][ny] == 0:
            # 주사위 바닥면의 수 복사
            map_lst[nx][ny] = dice[1]
        else:
            dice[1] = map_lst[nx][ny]
            map_lst[nx][ny] = 0
        answer.append(dice[0])
        x, y = nx, ny

for i in answer:
    print(i)
