# -*- coding: utf-8 -*-
import sys
from collections import deque


def select_attacker():
    # x, y, 공격력
    attacker, defender = [-1, -1, -1], [-1, -1, -1]

    # 공격력 작은, 행+열 큰, 열 큰 순서
    port.sort(key=lambda x: (x[2], -(x[0] + x[1]), -x[1]))

    # 공격자 선정
    for x, y, d in port:
        if attacker[2] == -1 or d < attacker[2]:
            attacker = [x, y, d]
        elif d == attacker[2]:
            # 이 좌표의 최근 공격 시간이 더 최근이면 변경
            if map_lst[x][y][1] > map_lst[attacker[0]][attacker[1]][1]:
                attacker = [x, y, d]

    # 방어자 선정
    for x, y, d in port[::-1]:
        if defender[2] == -1 or d > defender[2]:
            defender = [x, y, d]
        elif d == defender[2]:
            # 이 좌표의 최근 공격 시간이 더 오래전이면 변경
            if map_lst[x][y][1] < map_lst[defender[0]][defender[1]][1]:
                defender = [x, y, d]

    # 공격자 최근 공격 시간 갱신, 공격력 증가
    map_lst[attacker[0]][attacker[1]] = [attacker[2] + N + M, time]
    attacker[2] += N + M

    return attacker, defender


def bfs(attacker, defender):
    visited = [[-1 for _ in range(M)] for _ in range(N)]
    x, y, d = attacker
    tx, ty, td = defender

    queue = deque()
    queue.append([x, y, 0, [[x, y]]])
    visited[x][y] = 0
    while queue:
        x, y, distance, path = queue.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            # 범위 벗어나면 조정
            if 0 > nx or nx >= N or 0 > ny or ny >= M:
                nx = nx % N
                ny = ny % M

            # 벽이거나, 방문한 곳
            if map_lst[nx][ny][0] == 0 or visited[nx][ny] != -1:
                continue

            path.append([nx, ny])
            queue.append([nx, ny, distance + 1, path[:]])
            path.pop()

            visited[nx][ny] = distance + 1
            if (nx, ny) == (tx, ty):
                path.append([tx, ty])
                return visited, path

    return False, False


def attack(attacker, defender):
    """
    bfs로 경로 맵을 만든 뒤에, 우하좌상 순서로 다음 숫자가 있으면 연결하는 방식으로 구현
    bfs에서 공격에 관련된 경로 저장해서 나오도록 해야 함
    """
    global map_lst

    half_damage = attacker[2] // 2
    sx, sy = attacker[0], attacker[1]
    tx, ty = defender[0], defender[1]

    # 레이저 공격 가능 여부 판단
    visited, path = bfs(attacker, defender)
    if visited:
        for x, y in path:
            if (x, y) == (sx, sy):
                continue
            elif (x, y) != (tx, ty):
                map_lst[x][y][0] -= half_damage
            else:
                map_lst[x][y][0] -= attacker[2]
    # 포탄 공격
    else:
        path = [[sx, sy], [tx, ty]]
        map_lst[tx][ty][0] -= attacker[2]
        for i in range(8):
            nx = tx + dx8[i]
            ny = ty + dy8[i]
            # 범위 벗어나면 조정
            if 0 > nx or nx >= N or 0 > ny or ny >= M:
                nx = nx % N
                ny = ny % M

            if map_lst[nx][ny][0] <= 0 or [nx, ny] == [sx, sy] or [nx, ny] == [tx, ty]:
                continue

            map_lst[nx][ny][0] -= half_damage
            path.append([nx, ny])

    return path


def repair_port(path):
    global port

    new_port = []
    # 공격에 관련된 포탑들은 +1하면 안됨
    for x in range(N):
        for y in range(M):
            if [x, y] in path:
                map_lst[x][y][0] = max(map_lst[x][y][0], 0)

            elif map_lst[x][y][0] > 0:
                map_lst[x][y][0] += 1

            # 포탑 리스트 재정리
            if map_lst[x][y][0] > 0:
                new_port.append([x, y, map_lst[x][y][0]])

    port = new_port

    return


N, M, K = map(int, sys.stdin.readline().split())

# 공격력, 최근 공격 시간
map_lst = []
# x, y, 공격력
port = []
for x in range(N):
    tmp = list(map(int, sys.stdin.readline().split()))
    for y in range(M):
        if tmp[y] != 0:
            port.append([x, y, tmp[y]])

    map_lst.append([[i, 0] for i in tmp])

# 우 하 좌 상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

dx8 = [0, 1, 1, 1, 0, -1, -1, -1]
dy8 = [1, 1, 0, -1, -1, -1, 0, 1]

###
for time in range(1, K + 1):
    attacker, defender = select_attacker()

    path = attack(attacker, defender)
    repair_port(path)

    if len(port) == 1:
        break

port.sort(key=lambda x: -x[2])
print(port[0][2])

"""
10 10 20
995 3976 1850 0 0 0 0 0 2823 0
0 2197 4554 0 3991 0 0 0 0 0
2243 918 206 2051 0 0 0 0 0 2354
0 0 2211 394 3896 2763 0 0 3580 3094
0 0 4364 0 0 0 0 0 0 4990
0 0 0 0 0 0 736 0 1159 0
1374 0 2610 3165 3653 0 2651 0 0 0
4493 0 1423 0 2416 0 0 0 3580 0
0 4112 3779 0 3654 1247 0 0 132 712
92 2643 1459 4675 4838 0 2539 850 2040 2153

4168


경로를 bfs에서 저장해서 나와야 했음
안그러면 이상한 곳으로 들어가서 묶이는 케이스 존재

16:39 시작, 18:51 종료 (약 2시간 10분 소요)
"""
