'''
고대 문명 유적 탐사

start: 21:45
end:

회고:
    - loop 안에서 x, y를 같이 사용해서 값이 변하는 문제 발생;;
    - 디버깅도 어려움 이건,,,
    - 변수 관리 잘 하기

    # 조각 없어질 위치 표시
    for (_x, _y) in loc:
        reward_map[_x][_y] = 1

- 5x5 격자
- 유물 조각은 숫자 1~7로 표현

1. 탐사 진행
    - 3x3 격자를 선택해서 회전시킬 수 있음
    - 선택된 격자는 시계 방향으로 90도, 180도, 270도 중 하나의 각도만큼 회전시킬 수 있음
    - 가능한 회전의 방법 중, 유물 1차 획득 가치 최대화 >> 회전한 각도가 작은 방법 >> 회전 중심 좌표의 열 작은 >> 행이 작은 순서로 선택

2. 유물 획득
    - 3개 이상의 조각들이 연결된 경우, 조각이 모여 유물이 되고 사라짐
    - 유물의 가치는 모인 조각의 갯수와 같음
    - 유적의 벽면에 적힌 순서대로 조각이 사라진 위치가 채워짐
        - 열 번호가 작은 순 >> 행 번호가 큰 순
        - 조각의 수가 부족한 경우는 없음

3. 유물 연쇄 획득
    - 새로운 유물 조각이 생겨난 이후에도 3개 이상 연결된 조각을 없앰
    - 더 이상 유물이 될 수 없을 때까지 반복

- K번의 턴에 걸쳐 진행
- 각 턴마다 획득한 유물의 가치의 총합을 출력하는 프로그램 작성
- 탐사 과정에서 어떠한 방법을 사용하더라도 유물 획득이 불가능하면, 그 즉시 탐사 종료
    - 종료되는 턴에 아무 값도 출력하지 않음

'''

from collections import deque

import copy

def bfs(queue, tmp_map):
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

            # 같은 숫자를 가지고 있다면
            if tmp_map[nx][ny] == tmp_map[x][y]:
                visited[nx][ny] = 1
                queue.append((nx, ny))

    return loc


def cal_reward(tmp_map):
    global visited, reward_map

    visited = [[0 for _ in range(5)] for _ in range(5)]
    reward_map = [[0 for _ in range(5)] for _ in range(5)]
    queue = deque()

    reward_score = 0
    for x in range(5):
        for y in range(5):
            if not visited[x][y]:
                visited[x][y] = 1
                queue.append((x, y))
                loc = bfs(queue, tmp_map)

                if len(loc) >= 3:
                    reward_score += len(loc)

                    # 조각 없어질 위치 표시
                    for (_x, _y) in loc:
                        reward_map[_x][_y] = 1

    return reward_score


def rotate90(x, y):
    # (x,y) -> (y, 2-x)
    tmp_map = copy.deepcopy(map_lst)

    # 회전
    upper_x, upper_y = x - 1, y - 1
    for i in range(3):
        for j in range(3):
            tmp_map[j + upper_x][2 - i + upper_y] = map_lst[i + upper_x][j + upper_y]

    return cal_reward(tmp_map), tmp_map


def rotate180(x, y):
    # (x,y) -> (2-x, 2-y)
    tmp_map = copy.deepcopy(map_lst)

    # 회전
    upper_x, upper_y = x - 1, y - 1
    for i in range(3):
        for j in range(3):
            tmp_map[2 - i + upper_x][2 - j + upper_y] = map_lst[i + upper_x][j + upper_y]

    return cal_reward(tmp_map), tmp_map


def rotate270(x, y):
    # (x,y) -> (2-y, x)
    tmp_map = copy.deepcopy(map_lst)

    # 회전
    upper_x, upper_y = x - 1, y - 1
    for i in range(3):
        for j in range(3):
            tmp_map[2 - j + upper_x][i + upper_y] = map_lst[i + upper_x][j + upper_y]

    return cal_reward(tmp_map), tmp_map


def find():
    # (deg, x, y) order
    reward = 0
    rotate_info = [(0, 0, 0)]

    # 중심 좌표의 범위는 1~3
    for x in range(1, 4):
        for y in range(1, 4):
            # 90, 180, 270도 회전하면서 확인
            _reward, _ = rotate90(x, y)
            if _reward > reward:
                reward = _reward
                rotate_info = [(90, x, y)]
            elif _reward == reward:
                rotate_info.append((90, x, y))

            _reward, _ = rotate180(x, y)
            if _reward > reward:
                reward = _reward
                rotate_info = [(180, x, y)]
            elif _reward == reward:
                rotate_info.append((180, x, y))

            _reward, _ = rotate270(x, y)
            if _reward > reward:
                reward = _reward
                rotate_info = [(270, x, y)]
            elif _reward == reward:
                rotate_info.append((270, x, y))

    # 우선 순위에 맞게 sort (각도 작은 >> 열 작은 >>  행 작은)
    rotate_info.sort(key=lambda x:(x[0], x[2], x[1]))

    return reward, rotate_info[0]


def get_reward(rot_info):
    global cur_answer, map_lst

    deg, x, y = rot_info

    if deg == 90:
        _, new_map = rotate90(x, y)
    elif deg == 180:
        _, new_map = rotate180(x, y)
    elif deg == 270:
        _, new_map = rotate270(x, y)

    # 더 이상 유물이 생기지 않을 때까지 비우고 채우기 반복
    while True:
        score = cal_reward(new_map)
        if not score:
            map_lst = new_map
            return
        
        # 점수 추가
        cur_answer += score

        # 조각 채우기 (열 작을수록 >> 행 클수록)
        for y in range(5):
            for x in range(4, -1, -1):
                if reward_map[x][y]:
                    _num = num_lst.popleft()
                    new_map[x][y] = _num

    return


K, M = map(int, input().split())

# map은 5x5
map_lst = [list(map(int, input().split())) for _ in range(5)]

num_lst = deque(list(map(int, input().split())))

# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

answer = []
for k in range(K):
    cur_answer = 0

    reward, rot_info = find()

    # 유물 획득이 불가능하면
    if not reward:
        break

    get_reward(rot_info)

    # 정답 체크
    answer.append(cur_answer)

for i in answer:
    print(i, end=' ')
