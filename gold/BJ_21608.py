# -*- coding: utf-8 -*-
import sys


def find_loc(target, st_lst):
    """
    좋아하는 학생이 가장 많은 칸 + 비어있는 칸 갯수 동시에 찾도록
    """
    target_loc = [[-1, -1], [-1, -1]]
    for x in range(N):
        for y in range(N):
            if map_lst[x][y] != 0:
                continue
            else:
                attract, vacant = 0, 0
                for i in range(4):
                    nx = x + dir[i][0]
                    ny = y + dir[i][1]
                    if 0 > nx or nx >= N or 0 > ny or ny >= N:
                        continue
                    elif map_lst[nx][ny] == 0:
                        vacant += 1
                    elif map_lst[nx][ny] in st_lst:
                        attract += 1

                # 좋아하는 학생이 많으면 변경
                if attract > target_loc[1][0]:
                    target_loc[0] = [x, y]
                    target_loc[1] = [attract, vacant]
                elif attract == target_loc[1][0]:
                    # 빈 공간이 많은 칸으로 변경
                    if vacant > target_loc[1][1]:
                        target_loc[0] = [x, y]
                        target_loc[1] = [attract, vacant]
                    elif vacant == target_loc[1][1]:
                        # 행이 작은 칸
                        if x < target_loc[0][0]:
                            target_loc[0] = [x, y]
                        # 열이 작은 칸
                        elif x == target_loc[0][0] and y < target_loc[0][1]:
                            target_loc[0] = [x, y]

    [x, y] = target_loc[0]
    map_lst[x][y] = target

    return


def cal_satisfaction():
    answer = 0
    attract_lst = [0, 1, 10, 100, 1000]
    for x in range(N):
        for y in range(N):
            target = student[map_lst[x][y]]
            attract = 0
            for i in range(4):
                nx = x + dir[i][0]
                ny = y + dir[i][1]

                if 0 > nx or nx >= N or 0 > ny or ny >= N:
                    continue
                elif map_lst[nx][ny] in target:
                    attract += 1

            answer += attract_lst[attract]

    return answer


N = int(sys.stdin.readline())
student = dict()
for i in range(N**2):
    tmp = list(map(int, sys.stdin.readline().split()))
    student[tmp[0]] = set(tmp[1:])

map_lst = [[0 for _ in range(N)] for _ in range(N)]
dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]

for i in student:
    find_loc(i, student[i])

print(cal_satisfaction())

"""
1. 좋아하는 학생이 인접한 칸에 가장 많은 칸
2. 여러개면 비어있는 칸이 가장 많은 칸
3. 여러개면 행/열이 작은 칸
"""
