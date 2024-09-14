def print_map():
    for i in map_lst:
        print(i)

    return

'''
start : 18:48
end : 20:38

회고 : 
    - 인접한 변을 세는 기준을 숫자로만 바라봄
    - 그룹을 나누는 bfs를 먼저 돌리고, 나눠진 그룹을 가지고 점수를 계산하는 로직을 짜야 함

nxn 격자
각 칸의 색깔을 1 ~ 10 이하의 숫자

그룹 쌍의 조화로움:
    - (그룹 a에 속한 칸의 수 + 그룹 b에 속한 칸의 수 ) x 그룹 a를 이루고 있는 숫자 값 x 그룹 b를 이루고 있는 숫자 값 x 그룹 a와 그룹 b가 서로 맞닿아 있는 변의 수

회전 :
    - 십자 모양의 경우 통쩨로 반시계 90도 회전
    - 4개의 정사각형은 개별적으로 시계 방향으로 90도 회전

초기, 1회전, 2회전, 3회전 이후 예술 점수의 합을 구하는 프로그램

조화로움을 구할 때에는 bfs로 계속 돌면서, 다른 숫자 만나면 그 숫자에 대한 cnt 올려주도록 max (10 x 10) matrix 만들어짐
'''

import copy
from collections import deque


def rotate_line():
    global map_lst

    # 세로, 가로
    # line_set = [[(i, n//2) for i in range(n)], [(n//2, i) for i in range(n)]]

    new_map = copy.deepcopy(map_lst)

    # 세로 -> 가로 변환(정순서)
    for (x, y), (tx, ty) in zip(line_set[0], line_set[1]):
        new_map[tx][ty] = map_lst[x][y]

    # 가로 -> 세로 변환(역순서)
    for (x, y), (tx, ty) in zip(line_set[1], line_set[0][::-1]):
        new_map[tx][ty] = map_lst[x][y]

    map_lst = new_map

    return


def rotate_square(loc):
    global map_lst

    new_map = copy.deepcopy(map_lst)

    start_x, start_y = loc

    # 시작 위치부터 n//2개씩 가진 사각형 회전
    for x in range(n//2):
        for y in range(n//2):
            sx, sy = start_x + x, start_y + y
            nx, ny = start_x + y, start_y + (n//2 - 1 - x)
            new_map[nx][ny] = map_lst[sx][sy]

    map_lst = new_map

    return


def bfs_find_adjacent():
    global new_visited, queue, num_adjacent, num_matrix

    while queue:
        (x, y) = queue.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            # 벽을 만날 경우
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            elif new_visited[nx][ny]:
                continue

            cur_group, nxt_group = visited[nx][ny], visited[x][y]
            # 그룹이 같을 경우
            if cur_group == nxt_group:
                new_visited[nx][ny] = 1
                num_matrix[visited[x][y]] += 1
                queue.append((nx, ny))

            # 그룹이 다를 경우
            else:
                # 대각 성분 두 개를 다 더해줘야 함
                num_adjacent[cur_group][nxt_group] += 1
                num_adjacent[nxt_group][cur_group] += 1

    return


def bfs():
    global visited, queue

    while queue:
        (x, y) = queue.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            
            # 벽을 만날 경우
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            elif visited[nx][ny]:
                continue

            # 숫자가 같을 경우
            if map_lst[x][y] == map_lst[nx][ny]:
                visited[nx][ny] = group_num
                queue.append((nx, ny))

    return


def cal_score():
    global visited, queue, group_num, group

    # visited는 그룹의 숫자가 써진 맵
    visited = [[0 for _ in range(n)] for _ in range(n)]
    queue = deque()

    # grouping
    # visited를 돌면서, 방문하지 않은 곳들은 queue에 넣어줌
    group = dict()
    group_num = 0
    for x in range(n):
        for y in range(n):
            if not visited[x][y]:
                # t번 그룹, 숫자
                group_num += 1
                group[group_num] = map_lst[x][y]
                visited[x][y] = group_num
                queue.append((x,y))

                bfs()

    global num_matrix, num_adjacent, new_visited

    # 그룹 당 갯수, 그룹 간 인접한 변의 갯수 찾기
    # idx 0은 쓰지 않는 값
    num_matrix = [0 for _ in range(group_num + 1)]
    num_adjacent = [[0 for _ in range(group_num + 1)] for _ in range(group_num + 1)]

    new_visited = [[0 for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if not new_visited[x][y]:
                new_visited[x][y] = 1
                num_matrix[visited[x][y]] += 1
                queue.append((x,y))

                bfs_find_adjacent()

    # 계산 결과 가지고 score 계산, 우삼각행렬만 사용
    score = 0
    for cur_group in range(1, group_num+1):
        for tar_group in range(cur_group+1, group_num+1):
            if num_adjacent[cur_group][tar_group] != 0:
                # (갯수1 + 갯수2) * 값1 * 값2 * 변 수
                _tmp = (num_matrix[cur_group] + num_matrix[tar_group]) * group[cur_group] * group[tar_group] * num_adjacent[cur_group][tar_group]
                score += _tmp

    return score


n = int(input())
map_lst = [list(map(int, input().split())) for _ in range(n)]

start_loc = [(0, 0), (n // 2 + 1, 0), (0, n // 2 + 1), (n // 2 + 1, n // 2 + 1)]
line_set = [[(i, n//2) for i in range(n)], [(n//2, i) for i in range(n)]]

dx = [1, 0, -1, 0]
dy = [0, -1, 0, 1]

answer = 0
answer += cal_score()

for i in range(3):
    # 중앙 십자 모양 반시계 90도 회전
    rotate_line()

    # 각 사각형 부분 시계 90도 회전
    for loc in start_loc:
        rotate_square(loc)

    # 점수 계산
    answer += cal_score()

print(answer)

'''
5
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25
'''