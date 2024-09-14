
'''
고대 문명 유적 탐사

start : 21:10
end : 23:10 (중간에 끊김, 약 한시간 반)

회고 :
    - 상반기에 코테 가서 헤맸던 문제
    - 5x5 격자인데 MxM으로 봐서 이번에도 디버깅함
    - 불필요한 계산을 어떻게 줄일 수 있을까 고민해야 함
        - visited를 인자로 타고 타고 넘기나? map을? score 계산과 별개로 유물 획득한 위치는 어떻게 저장하고 비우지?

5x5 격자, 유물의 종류는 7가지 (1~7로 표현)

1. 탐사 진행
    - 3x3 격자 선택
    - 3x3 격자 회전
    - 선택된 격자는 90, 180, 270도 시계방향으로 회전 가능
    - 유물 1차 획득 가치를 극대화 >> 회전한 각도가 가장 작은 방법 선택 >> 회전 중심점의 열이 작은 >> 행이 작은

2. 유물 획득
    - 유물 1차 획득
        - 상하좌우로 인접한 유물 조각은 모두 연결
        - 3개 이상 연결된 경우, 유물 획득 (조각 갯수만큼 가치), 조각 사라짐
    - 숫자 채우기
        - 유적 벽면에 1~7 사이 숫자가 M개 적힘
        - 사라진 위치에는 벽면의 숫자가 적힌 순서대로 조각 들어감
        - 열 작은 순 >> 행 번호가 큰 순
        - 생겨날 조각의 수는 충분
    - 유물 연쇄 획득
        - 조각 생겨난 이후에도 3개 이상 연결될 수 있음
        - 더이상 3개 이상이 연결되지 않을 때까지 반복

- K번의 턴 진행
- 각 턴마다 획득한 유물의 가치를 출력
- 탐사 진행 과정에서 어떠한 방법을 사용하더라도 유물 획득 못할 경우, 그 즉시 종료 -> 이 턴에는 출력 없음
'''

from collections import deque

import copy


def bfs(queue, tmp_lst):
    cnt = 1

    # 칸 비울 칸
    loc = []
    while queue:
        x, y = queue.popleft()
        loc.append((x, y))
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if nx < 0 or nx >= 5 or ny < 0 or ny >= 5:
                continue
            elif visited[nx][ny]:
                continue

            # 숫자가 같으면 추적
            if tmp_lst[x][y] == tmp_lst[nx][ny]:
                visited[nx][ny] = 1
                queue.append((nx, ny))
                cnt += 1

    # 3개 이상이라면 칸 비움
    if cnt >= 3:
        for (tx, ty) in loc:
            reward_map[tx][ty] = 1

        return cnt

    return 0

def cal_score(tmp_map):
    global visited, reward_map

    # 지나간 자리 체크
    reward_map = [[0 for _ in range(5)] for _ in range(5)]
    
    queue = deque()
    visited  = [[0 for _ in range(5)] for _ in range(5)]
    
    # 전체 순회하면서 빈 칸 체크
    total_cnt = 0
    for x in range(5):
        for y in range(5):
            if not visited[x][y]:
                visited[x][y] = 1
                queue.append((x, y))
                cnt = bfs(queue, tmp_map)

                if cnt:
                    total_cnt += cnt

    return total_cnt


def rotate90(x, y):
    tmp_map = copy.deepcopy(map_lst)
    
    # upper_left 좌표
    lx, ly = x-1, y-1

    # (x, y) -> (y, 2-x)
    for i in range(3):
        for j in range(3):
            tmp_map[j + lx][2-i + ly] = map_lst[i + lx][j + ly]

    return tmp_map, cal_score(tmp_map)


def rotate180(x, y):
    tmp_map = copy.deepcopy(map_lst)

    # upper_left 좌표
    lx, ly = x - 1, y - 1

    # (x, y) -> (2-x, 2-y)
    for i in range(3):
        for j in range(3):
            tmp_map[2-i + lx][2-j + ly] = map_lst[i + lx][j + ly]

    return tmp_map, cal_score(tmp_map)


def rotate270(x, y):
    tmp_map = copy.deepcopy(map_lst)

    # upper_left 좌표
    lx, ly = x - 1, y - 1

    # (x, y) -> (2-y, x)
    for i in range(3):
        for j in range(3):
            tmp_map[2-j + lx][i + ly] = map_lst[i + lx][j + ly]

    return tmp_map, cal_score(tmp_map)


def rotate_map():
    global map_lst

    max_score = 0

    # (회전 각도, 행, 열)
    tmp_rotations = []

    # 가치가 큰 >> 회전 각도가 작은 >> 열 작은 >> 행 작은
    for y in range(1, 4):
        for x in range(1, 4):
            _, score = rotate90(x, y)
            if score > max_score:
                max_score = score
                tmp_rotations = [(90, x, y)]
            elif score == max_score:
                tmp_rotations.append((90, x, y))

            _, score = rotate180(x, y)
            if score > max_score:
                max_score = score
                tmp_rotations = [(180, x, y)]
            elif score == max_score:
                tmp_rotations.append((180, x, y))

            _, score = rotate270(x, y)
            if score > max_score:
                max_score = score
                tmp_rotations = [(270, x, y)]
            elif score == max_score:
                tmp_rotations.append((270, x, y))

    if not max_score:
        return 0
    else:
        tmp_rotations.sort(key=lambda x:(x[0], x[2], x[1]))

        deg, tx, ty = tmp_rotations[0]
        if deg == 90:
            new_map, _ = rotate90(tx, ty)
        elif deg == 180:
            new_map, _ = rotate180(tx, ty)
        elif deg == 270:
            new_map, _ = rotate270(tx, ty)

        # map 회전된 결과로 return해야 함
        map_lst = new_map

        return 1


def fill_number():
    for y in range(5):
        for x in range(4, -1, -1):
            # 만약 유물 획득한 칸이라면
            if reward_map[x][y]:
                map_lst[x][y] = spare_num.popleft()

    return


K, M = map(int, input().split())

map_lst = [list(map(int, input().split())) for _ in range(5)]
spare_num = deque(list(map(int, input().split())))

# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

answer = []
for _ in range(K):
    flag = rotate_map()
    if not flag:
        break

    round_score = 0
    while True:
        cur_score = cal_score(map_lst)
        if not cur_score:
            break
        else:
            round_score += cur_score

        fill_number()

    answer.append(round_score)

for i in answer:
    print(i, end=' ')
