def print_map():
    for i in map_lst:
        print(i)

    return

'''
start : 21:25
end : 22:50

회고 :
    - remove_map을 만드는 조건을 잘못 봄 (나무가 아예 없는 위치의 경우 더 이상 살충제 전파가 안됨)

nxn 격자
제초제는 K의 범위만큼 대각선으로 퍼짐, 벽이 있는 경우 가로막힘

1. 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장
2. 벽 / 나무 / 제초제 모두 없는 칸에 번식 진행
    - 번식이 가능한 칸의 개수만큼 나누어진 그루 수만큼 번식, 나머지는 버림
3. 제초제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸에 제초제를 뿌림
    - 나무가 있는 칸에 뿌리면, 4개의 대각선 방향으로 K칸 만큼 전파
    - 전파 도중에 벽이 있거나 나무가 아예 없는 칸이 있는 경우 그 이후로는 전파되지 않음
    - c년 만큼 제초제가 남아있다가 c+1년에 사라짐

    - 박멸시키는 나무의 수가 동일한 칸 -> 행 작은 >> 열 작은 순서
'''

import copy


def grow():
    global map_lst, blank_map

    new_map = copy.deepcopy(map_lst)
    blank_map = [[0 for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if map_lst[x][y] <= 0:
                continue

            # 네 방향 체크
            num = 0
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]

                if nx < 0 or nx >= n or ny < 0 or ny >= n:
                    continue
                elif map_lst[nx][ny] == 0:
                    if remove_map[nx][ny] == 0:
                        blank_map[x][y] += 1
                    continue
                elif map_lst[nx][ny] == -1:
                    continue

                num += 1

            # 나무 성장
            new_map[x][y] += num

    map_lst = new_map

    return


def spread():
    global map_lst

    new_map = copy.deepcopy(map_lst)
    for x in range(n):
        for y in range(n):
            if map_lst[x][y] == 0:
                continue
            elif not blank_map[x][y]:
                continue

            # 네 방향 체크
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]

                if nx < 0 or nx >= n or ny < 0 or ny >= n:
                    continue
                # 빈 칸을 대상으로 확산됨
                elif map_lst[nx][ny] != 0:
                    continue
                # 제초제가 뿌려진 곳의 경우
                elif remove_map[nx][ny]:
                    continue

                new_map[nx][ny] += (map_lst[x][y] // blank_map[x][y])

    map_lst = new_map

    return


def remove_tree():
    global map_lst, remove_map, answer
    
    # 행 작은 >> 열 작은, 없애는 나무의 수
    loc = (-1, -1)
    best_num = 0
    for x in range(n):
        for y in range(n):
            if map_lst[x][y] <= 0:
                continue

            remove_num = map_lst[x][y]

            # 네 대각선 확인, 각 대각선에 대해서 k번 진행
            for i in range(4):
                nx, ny = x, y
                for _k in range(k):
                    nx += diag_x[i]
                    ny += diag_y[i]

                    if nx < 0 or nx >= n or ny < 0 or ny >= n:
                        break
                    elif map_lst[nx][ny] <= 0:
                        break

                    remove_num += map_lst[nx][ny]

            if remove_num > best_num:
                best_num = remove_num
                loc = (x, y)

    # best 값 기준으로 나무 없애기
    answer += best_num
    for i in range(4):
        nx, ny = loc
        map_lst[nx][ny] = 0
        remove_map[nx][ny] = c + 1

        for _k in range(k):
            nx += diag_x[i]
            ny += diag_y[i]

            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                break
            elif map_lst[nx][ny] <= 0:
                remove_map[nx][ny] = c + 1
                break

            map_lst[nx][ny] = 0
            remove_map[nx][ny] = c + 1
    
    # remove_map의 값 줄이기
    for x in range(n):
        for y in range(n):
            remove_map[x][y] = max(0, remove_map[x][y] - 1)

    return

# 격자의 크기 n, 박멸이 진행되는 년 수 m, 제초제의 확산 범위 k, 제초제가 남아있는 년 수 c
n, m, k, c = map(int, input().split())

map_lst = [list(map(int, input().split())) for _ in range(n)]
remove_map = [[0 for _ in range(n)] for _ in range(n)]

# 우 하 좌 상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

# 1시 5시 7시 11시
diag_x = [-1, 1, 1, -1]
diag_y = [1, 1, -1, -1]

answer = 0
for _ in range(m):
    grow()
    spread()
    remove_tree()


print(answer)