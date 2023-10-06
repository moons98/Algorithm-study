# -*- coding: utf-8 -*-
import sys
from collections import deque


def check_available(x, y, side_dir):
    """
    벽은 0이면 해당칸 위, 1이면 해당칸 오른쪽이 막힌 것
    """
    tx = x + dx[side_dir]
    ty = y + dy[side_dir]

    if side_dir == 0 and (x, y) in wall["1"]:
        return False
    elif side_dir == 1 and (tx, ty) in wall["0"]:
        return False
    elif side_dir == 2 and (tx, ty) in wall["1"]:
        return False
    elif side_dir == 3 and (x, y) in wall["0"]:
        return False

    if 0 > tx or tx >= R or 0 > ty or ty >= C:
        return False

    return (tx, ty)


def work_fan():
    """
    방향이 1이면 퍼지는게 1, 1+0, 1+2, ...
    먼저 사이드 방향이 윗방향 / 아랫방향이 있는지부터 확인
    """
    for x, y, dir in fan:
        visited = [[0 for _ in range(C)] for _ in range(R)]
        side_dir = [(dir + 1) % 4, (dir - 1) % 4]

        nx = x + dx[dir]
        ny = y + dy[dir]
        map_lst[nx][ny] += 5

        queue = deque([[nx, ny, 4]])
        while queue:
            x, y, up_temp = queue.popleft()
            # 사이드로 갈 수 있는 지 확인
            new_loc = [(x, y)]
            for j in side_dir:
                loc = check_available(x, y, j)
                if loc:
                    new_loc.append(loc)
            # 새 좌표에 대해서 가능 여부 및 방문 확인 후 온풍기 동작
            for nx, ny in new_loc:
                loc = check_available(nx, ny, dir)
                if loc and not visited[loc[0]][loc[1]]:
                    map_lst[loc[0]][loc[1]] += up_temp
                    visited[loc[0]][loc[1]] = 1
                    if up_temp > 1:
                        queue.append([loc[0], loc[1], up_temp - 1])

    return


def temp_control():
    new_map = [i[:] for i in map_lst]
    for x, val in enumerate(map_lst):
        for y, val2 in enumerate(val):
            for i in range(4):
                loc = check_available(x, y, i)
                if loc:
                    nx, ny = loc[0], loc[1]
                    temp_sub = (val2 - map_lst[nx][ny]) // 4
                    if temp_sub > 0:
                        new_map[x][y] -= temp_sub
                        new_map[nx][ny] += temp_sub

    return new_map


def decrease_temp():
    """
    모서리가 중복으로 줄어드는 경우 주의
    """
    loc = set()
    for x in [0, R - 1]:
        for y in range(C):
            loc.add((x, y))

    for y in [0, C - 1]:
        for x in range(R):
            loc.add((x, y))

    for x, y in list(loc):
        if map_lst[x][y] > 0:
            map_lst[x][y] -= 1

    return


def check_temp():
    for x, y in target:
        if map_lst[x][y] < K:
            return False

    return True


R, C, K = map(int, sys.stdin.readline().split())

#  오, 왼, 상, 하 -> 오 하 왼 상
trans_dir = [0, 2, 3, 1]
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

map_lst = []
fan = []
target = []
for i in range(R):
    tmp = list(map(int, sys.stdin.readline().split()))
    for idx, j in enumerate(tmp):
        if 1 <= j <= 4:
            fan.append((i, idx, trans_dir[j - 1]))
        elif j == 5:
            target.append((i, idx))

    map_lst.append([0 for _ in range(C)])

W = int(sys.stdin.readline())

wall = {"0": [], "1": []}
for _ in range(W):
    x, y, d = map(int, sys.stdin.readline().split())
    wall[str(d)].append((x - 1, y - 1))

answer = 1
while True:
    if answer >= 101:
        break

    work_fan()
    map_lst = temp_control()
    decrease_temp()

    if check_temp():
        break
    else:
        answer += 1

print(answer)

"""
무조건 횡 이동부터 수행하고 직진으로 바람이 지나갈 수 있는지 판단

1. 온풍기에서 바람이 나옴
2. 온도 조절 (온도차/4)
3. 가장 바깥쪽 칸의 온도가 1씩 감소
4. 초콜릿 하나 증가
5. 확인하고자 하는 칸의 온도가 K 이상인지 확인, 아니면 다시 반복

벽이 있는 경우에는 온도가 조절되지 않는다 조건을 놓침
가장 바깥쪽 칸이 0과 접한 부분이 아니었음
양 꼭짓점의 부분이 중복으로 온도가 줄어드는 경우를 놓침
"""
