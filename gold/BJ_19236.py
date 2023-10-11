# -*- coding: utf-8 -*-
import copy
import sys


def check_loc(num, tmp_map):
    for x in range(4):
        for y in range(4):
            # 번호가 일치하면 움직임
            if tmp_map[x][y][0] == num:
                return x, y, tmp_map[x][y][1]

    return False


def dfs(sx, sy, num_fish, tmp_map):
    global answer

    # 물고기 먹음, 상어를 따로 -1 처리할 필요가 없음
    num_fish += tmp_map[sx][sy][0]
    tmp_map[sx][sy][0] = 0

    # 물고기 이동
    for i in range(1, 17):
        if check_loc(i, tmp_map):
            x, y, d = check_loc(i, tmp_map)
            for _ in range(8):
                nx = x + dx[d]
                ny = y + dy[d]
                if 0 > nx or nx >= 4 or 0 > ny or ny >= 4 or (nx, ny) == (sx, sy):
                    d = (d + 1) % 8
                    continue
                tmp_map[x][y] = tmp_map[nx][ny][:]
                tmp_map[nx][ny] = [i, d]
                break

    # 상어 이동
    nd = tmp_map[sx][sy][1]
    for i in range(1, 4):
        nx = sx + dx[nd] * i
        ny = sy + dy[nd] * i
        # 종료 조건
        if 0 > nx or nx >= 4 or 0 > ny or ny >= 4 or tmp_map[nx][ny][0] == 0:
            answer = max(answer, num_fish)
            continue

        dfs(nx, ny, num_fish, copy.deepcopy(tmp_map))

    return


map_lst = [[0 for _ in range(4)] for _ in range(4)]

fish = dict()
for x in range(4):
    tmp = list(map(int, sys.stdin.readline().split()))
    for y in range(0, 8, 2):
        # 번호, 방향
        map_lst[x][y // 2] = [tmp[y], tmp[y + 1] - 1]

# ↑, ↖, ←, ↙, ↓, ↘, →, ↗
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

answer = 0
dfs(0, 0, answer, map_lst)
print(answer)

"""
1. (0,0)으로 상어가 들어감
   - 먹은 물고기의 방향을 가짐
2. 번호가 작은 물고기부터 이동
   - 다른 물고기가 있는 칸으로 이동할 때에는 둘의 자리를 바꿈
3. 상어 이동
   - 이동할 수 있는 곳이 없으면 종료
   
상어가 먹을 수 있는 물고기 번호 합의 최댓값 구하기

map_lst와 fish를 둘 다 운용하려 했는데, 총 순회하면서 찾는 값이 4x4x16이 최대라서 굳이 할 필요 없음
물고기를 먹음 처리를 dfs 처음에 하는 이유는, visited와 같이 먹음 처리를 한 후 풀어줘야 하기 때문
'물고기가 없는 칸으로는 이동할 수 없다' 조건을 놓침

종료 조건에 tmp_map[nx][ny][0] == 0: 추가하면서 안되는 좌표가 중간에 끼어있을 수 있게됨
따라서 return이 아닌 continue를 사용했어야 함!!!
"""
