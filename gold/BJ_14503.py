# -*- coding: utf-8 -*-
import sys


def print_map(tmp_lst):
    print()
    print(robot, answer)
    for i in tmp_lst:
        print(i)

    return


def check_available(x, y):
    if x < 0 or x >= N or y < 0 or y >= M:
        return False
    elif map_lst[x][y] == 1:
        return False
    else:
        return True


def clean_tile(nx, ny):
    global answer

    if map_lst[nx][ny] == 0:
        map_lst[nx][ny] = 2
        answer += 1

    return


def move_robot(robot):
    x, y, dir = robot

    # 청소되지 않은 빈 칸 찾기, 있으면 움직임
    for _ in range(4):
        # 반시계로 방향 수정
        dir = (dir - 1) % 4

        # 움직임 확인
        nx, ny = x + dx[dir], y + dy[dir]
        if map_lst[nx][ny] == 0:
            robot[:2] = [nx, ny]
            break

    # 청소되지 않은 빈 칸이 없으면 후진
    if robot[:2] == [x, y]:
        if check_available(x - dx[dir], y - dy[dir]):
            robot[:2] = [x - dx[dir], y - dy[dir]]

    # 방향 고정
    robot[2] = dir

    # 움직인 경우에는 청소, 후진도 못한 경우에는 중지
    if robot[:2] != [x, y]:
        clean_tile(*robot[:2])
    else:
        return False

    return True


N, M = map(int, sys.stdin.readline().split())
robot = list(map(int, sys.stdin.readline().split()))

# 0은 청소되지 않은 칸, 1은 벽
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 로봇 위치 청소
answer = 0
clean_tile(*robot[:2])

flag = True
while flag:
    flag = move_robot(robot)

print(answer)

"""
1. 청소되지 않은 경우, 칸 청소
2. 주변 칸 중 청소되지 않은 빈 칸이 없으면
    - 후진 가능하면 후진, 방향 유지
    - 후진할 수 없으면 작동 멈춤
3. 청소되지 않은 빈 칸이 있으면
    - 반시계 90도 회전
    - 앞 칸이 청소 가능하면 전진
"""
