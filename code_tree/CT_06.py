# -*- coding: utf-8 -*-
import sys


def move():
    global answer, participant

    ex, ey = exit_loc

    for idx, (x, y) in enumerate(participant):
        # 행이동 먼저 시도
        if ex != x:
            nx, ny = x, y
            if ex > nx:
                nx += 1
            else:
                nx -= 1

            if not map_lst[nx][ny]:
                participant[idx] = (nx, ny)
                answer += 1
                continue

        if ey != y:
            nx, ny = x, y
            if ey > ny:
                ny += 1
            else:
                ny -= 1

            if not map_lst[nx][ny]:
                participant[idx] = (nx, ny)
                answer += 1
                continue

    new_participant = [i for i in participant if i != exit_loc]
    participant = new_participant

    return


def find_square():
    global sx, sy, square_size

    ex, ey = exit_loc
    tx, ty, distance = n, n, 20

    for x, y in participant:
        # 참가자와 출구 사이 사각형 한 변의 길이 구하기
        d = max(abs(ex - x), abs(ey - y))

        lr_x, lr_y = max(ex, x), max(ey, y)
        ul_x, ul_y = max(0, lr_x - d), max(0, lr_y - d)

        # 거리가 작은 경우 lr 갱신 -> max 때리고 d만큼 빼서 ul 구하기
        if d == distance:
            if ul_x < tx:
                tx, ty = ul_x, ul_y
            elif ul_x == tx and ul_y < ty:
                tx, ty = ul_x, ul_y
        elif d < distance:
            tx, ty = ul_x, ul_y
            distance = d

    sx, sy, square_size = tx, ty, distance

    return


def rotate():
    global participant, exit_loc

    # ul, lr 좌표 구하기
    ul_x, ul_y = sx, sy
    lr_x, lr_y = sx + square_size, sy + square_size

    # 내구도 감소
    for x in range(ul_x, lr_x + 1):
        for y in range(ul_y, lr_y + 1):
            if map_lst[x][y] > 0:
                map_lst[x][y] -= 1

    # 정사각형 회전
    for x in range(ul_x, lr_x + 1):
        for y in range(ul_y, lr_y + 1):
            rx, ry = x - ul_x, y - ul_y
            next_patch[ry + ul_x][square_size - rx + ul_y] = map_lst[x][y]

    # map_lst에 next_patch 값 갱신
    for x in range(ul_x, lr_x + 1):
        for y in range(ul_y, lr_y + 1):
            map_lst[x][y] = next_patch[x][y]

    # 사람 회전
    for idx, (x, y) in enumerate(participant):
        # 정사각형 내에 있을 때만 회전 -> 잔차 구해서 더하는 방식
        if ul_x <= x <= lr_x and ul_y <= y <= lr_y:
            rx, ry = x - ul_x, y - ul_y
            participant[idx] = (ry + ul_x, square_size - rx + ul_y)

    # 출구 회전
    ex, ey = exit_loc
    rx, ry = ex - ul_x, ey - ul_y
    exit_loc = (ry + ul_x, square_size - rx + ul_y)

    return


def print_map():
    for i in map_lst:
        print(i)
    print()


"""
### 메이즈 러너

1. 미로는 NxN 격자, (r,c) 좌표, M명의 참가자

2. 미로의 각 칸은 세 가지 상태 존재
    - 빈 칸 : 참가자가 이동 가능
    - 벽
        이동 불가, 1~9 사이의 내구도
        회전 시, 내구도가 1씩 깎임
        내구도가 0이 되면 -> 빈칸으로 바뀜
    - 출구 : 참가자가 도착하면, 즉시 탈출
   
### 동작 
 
3. 1초마다 참가자는 한 칸씩 움직임
    - 최단 거리는 abs(x) + abs(y)
    - 참가자는 동시에 움직임 -> 한 칸에 2명 이상 존재 가능
    - 상하좌우 움직일 수 있음 -> 상하 움직임 >> 좌우 움직임
    - 움직일 수 없으면 그대로

4. 미로 회전
    - 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형을 잡음
    - 2개 이상이라면 r 작을수록 >> c 작을수록 우선 선택 
    - 시계방향으로 정사각형 90도 회전, 회전된 벽은 내구도 1씩 깎임

K초 동안 반복, K초 전에 모든 참가자가 탈출하면 게임 끝
모든 참가자들의 이동 거리 합과 출구 좌표 출력

sol)
    - 거리 직접 계산하기
    - dfs를 굳이 돌 필요가 없음
    - 같은 거리일 때 좌측 상단을 기준으로 봐야됨
    - 그렇지 않으면 좌표가 0보다 작아져서 실제로는 더 밀려나는 정사각형이 잡힘

"""

n, m, k = map(int, sys.stdin.readline().split())

map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]
next_patch = [[0 for _ in range(n)] for _ in range(n)]

# 참가자 좌표
participant = []
for _ in range(m):
    x, y = map(int, sys.stdin.readline().split())
    participant.append((x - 1, y - 1))

# 출구 좌표
x, y = map(int, sys.stdin.readline().split())
exit_loc = (x - 1, y - 1)

# 참가자 이동 거리 합 기록
answer = 0

# 회전해야 하는 최소 정사각형 정보
sx, sy, square_size = 0, 0, 0


for _ in range(k):
    move()

    # 모든 사람이 탈출했으면 종료
    if not participant:
        break

    find_square()
    rotate()

print(answer)
print(exit_loc[0] + 1, exit_loc[1] + 1)
