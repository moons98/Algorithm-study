# -*- coding: utf-8 -*-
import copy
import sys


def rotate_belt():
    global idx, num_remove
    idx = (idx - 1) % (2 * N)
    num_remove = (num_remove - 1) % (2 * N)

    # 도착 위치일 경우 삭제
    if visited[num_remove] == 1:
        robot_loc.remove(num_remove)
        visited[num_remove] = 0

    return


def move_robot():
    global robot_loc

    new_robot = []

    # 처음 올린 로봇부터 움직임
    for r in robot_loc:
        new_loc = (r + 1) % (2 * N)
        # 그 칸이 로봇이 없고, 내구도 1 이상 -> 움직일 수 있음
        if visited[new_loc] == 0 and belt[new_loc] > 0:
            visited[r] = 0
            belt[new_loc] -= 1

            # 내리는 위치일 경우에는 내구도 감소만 하고 위치 갱신 하지 않음!!
            if new_loc == num_remove:
                continue

            # 움직임 처리
            visited[new_loc] = 1
            new_robot.append(new_loc)
        else:
            new_robot.append(r)

    robot_loc = new_robot

    return


def add_robot():
    if belt[idx] > 0 and visited[idx] == 0:
        robot_loc.append(idx)
        visited[idx] = 1
        belt[idx] -= 1

    return


def check_finish():
    global answer

    if belt.count(0) >= K:
        return False
    else:
        answer += 1

    return True


N, K = map(int, sys.stdin.readline().split())
num_remove = N - 1
belt = list(map(int, sys.stdin.readline().split()))

visited = [0 for _ in range(2 * N)]
robot_loc = []
idx = 0


def print_state():
    print()
    print("idx", idx, "num_remove", num_remove)
    print("belt", belt)
    print("robot", robot_loc)
    print("visited", visited)

    return


answer = 1
flag = True
while flag:
    rotate_belt()
    move_robot()
    add_robot()

    flag = check_finish()

print(answer)

"""
1. 벨트 + 로봇 회전 (idx만 바꿔주면 됨)
2. 가장 먼저 벨트에 올라간 로봇부터 회전 가능하면 회전
    - 움직이고자 하는 칸에 로봇 없음, 내구도 1 이상
    - 이동 or 로봇 올리면 그 칸의 내구도 1 감소
    - 내리는 위치에 도달하면 그 즉시 내림 -> 내리는 위치가 N!!
3. 내구도 0 아니면 로봇 올림
4. 내구도 0인 칸의 개수가 K개 이상이면 종료, 아니면 1번으로 돌아감

## 1단계
1 2 1 2 1 2

2 1 2 1 2 1

'1' 1 2 1 2 1

## 2단계
1 '1' 1 2 1 2

1 1 '0' 2 1 2

'0' 1 '0' 2 1 2
"""
