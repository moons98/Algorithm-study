# -*- coding: utf-8 -*-
import sys


def fish_move():
    global map_lst
    """
    2. 물고기가 한 칸 이동
       - 상어, 물고기 냄새 있는 칸은 이동 불가
       - 이동 가능한 칸이 있을때까지 반시계 방향으로 45도 회전
       - 그럼에도 이동 불가하면 이동하지 않음
    """
    new_map = [[[] for _ in range(4)] for _ in range(4)]
    for fx in range(4):
        for fy in range(4):
            for d in map_lst[fx][fy]:
                flag = False
                for _ in range(8):
                    nx = fx + dir[d][0]
                    ny = fy + dir[d][1]
                    if (
                        0 > nx
                        or nx >= 4
                        or 0 > ny
                        or ny >= 4
                        or smell_map[nx][ny]
                        or (nx, ny) == shark
                    ):
                        d = (d - 1) % 8
                    else:
                        new_map[nx][ny].append(d)
                        flag = True
                        break
                if not flag:
                    new_map[fx][fy].append(d)

    map_lst = new_map

    return


def dfs(sx, sy, t, path, num_fish):
    """
    3. 상어가 3칸 이동 (dfs)
       - 상하좌우 인접한 칸으로 이동 가능
       - 물고기가 있는 칸을 지나면, 물고기 사라지고, 냄새가 남음
       - 가장 많은 물고기를 잡아먹는 방법으로 이동 (여러가지라면 사전순)
    """
    global all_path, max_fish
    # 종료 조건
    if t == 3:
        if num_fish > max_fish:
            max_fish = num_fish
            all_path = path[:]
        return

    for i in range(4):
        nx = sx + shark_dir[i][0]
        ny = sy + shark_dir[i][1]
        if 0 > nx or nx >= 4 or 0 > ny or ny >= 4:
            continue

        path.append(i)
        if not visited[nx][ny]:
            visited[nx][ny] = 1
            dfs(nx, ny, t + 1, path, num_fish + len(map_lst[nx][ny]))
            visited[nx][ny] = 0
        # 방문했던 곳은 물고기를 중복으로 세면 안됨
        else:
            dfs(nx, ny, t + 1, path, num_fish)

        path.pop()

    return


def after_dfs():
    global shark

    (sx, sy) = shark
    for i in all_path:
        sx += shark_dir[i][0]
        sy += shark_dir[i][1]
        if map_lst[sx][sy]:
            smell_map[sx][sy] = 3
            map_lst[sx][sy] = []

    shark = (sx, sy)

    return


def smell_remove():
    for x in range(4):
        for y in range(4):
            smell_map[x][y] = max(0, smell_map[x][y] - 1)

    return


def copy_fish():
    global map_lst

    for x in range(4):
        for y in range(4):
            map_lst[x][y] += copy_map[x][y]

    return


##
M, S = map(int, sys.stdin.readline().split())

map_lst = [[[] for _ in range(4)] for _ in range(4)]
for _ in range(M):
    fx, fy, d = map(int, sys.stdin.readline().split())
    map_lst[fx - 1][fy - 1].append(d - 1)

smell_map = [[0 for _ in range(4)] for _ in range(4)]
sx, sy = map(int, sys.stdin.readline().split())
shark = (sx - 1, sy - 1)

dir = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
shark_dir = [(-1, 0), (0, -1), (1, 0), (0, 1)]

visited = [[0 for _ in range(4)] for _ in range(4)]

for i in range(S):
    copy_map = [i[:] for i in map_lst]
    fish_move()

    # 2. 물고기 이동
    all_path, max_fish = [], -1
    # sx, sy, 움직인 횟수, 경로, 먹은 물고기
    dfs(shark[0], shark[1], 0, [], 0)
    after_dfs()

    smell_remove()
    copy_fish()

answer = 0
for x in range(4):
    for y in range(4):
        answer += len(map_lst[x][y])

print(answer)

"""
1. 복제 마법 시전
2. 물고기가 한 칸 이동 
   - 상어, 물고기 냄새 있는 칸은 이동 불가
   - 이동 가능한 칸이 있을때까지 반시계 방향으로 45도 회전
   - 그럼에도 이동 불가하면 이동하지 않음
3. 상어가 3칸 이동
   - 상하좌우 인접한 칸으로 이동 가능
   - 물고기가 있는 칸을 지나면, 물고기 사라지고, 냄새가 남음
   - 가장 많은 물고기를 잡아먹는 방법으로 이동 (여러가지라면 사전순)
4. 두 번 전의 연습에서 생긴 물고기 냄새가 사라짐
5. 복제된 물고기 등장

dfs 재귀로 구현하는 방식에 실수 (함수 속 함수로 dfs 호출하는 경우 visited나 path 전역 지역변수 체킹하는 것)
복제된 물고기는 시작점에 있으므로 visited가 continue 조건으로 들어가면 안됨!!
"""
