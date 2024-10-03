
'''
냉방 시스템

start: 10:45
end: 12:30

회고 :
    - power가 0 이하가 될 때에도 계산을 하게 만듦
    - 시간 초과: set 자료구조의 경우, 해시 충돌이 빈번하게 발생할 경우 O(n)까지 시간복잡도가 떨어질 수 있음, 평균적으로는 O(1)


- 0~5 사이의 숫자로 이루어진 nxn 격자
    - 0: 빈 공간, 1: 사무실, 2~5: 에어컨(좌상우하),

1. 에어컨 바람
    - 가는 방향에 벽이 있으면 전파되지 않음
    - 시원한 정도는 이전 위치 -1
    - 새로운 시원함은 모든 에어컨으로부터 나오는 시원함의 합

2. 시원한 공기의 섞임
    - 시원함이 높은 곳에서 낮은 곳으로 [시원함의 차이 / 4] 만큼 전파
    - 동시에 일어남, 벽을 사이에 두고는 일어나지 않음

3. 외벽에 있는 칸에 대해서 시원함이 1씩 감소

- 모든 사무실에서의 시원함이 k 이상이 될 때까지 반복
'''
import copy

from collections import deque

def check_available(_x, _y, _s):
    if (_x, _y, _s) in wall:
        return False
    else:
        nxt_x, nxt_y, nxt_s = _x + dx[_s], _y + dy[_s], (_s + 2) % 4

        if nxt_x < 0 or nxt_x >= n or nxt_y < 0 or nxt_y >= n:
            return False
        elif visited[nxt_x][nxt_y]:
            return False
        elif (nxt_x, nxt_y, nxt_s) in wall:
            return False

    return True


def move():
    global visited, pre_cool_map

    pre_cool_map = [[0 for _ in range(n)] for _ in range(n)]

    # 에어컨 마다 계산
    for (ax, ay, s) in air_conditioner:
        power = 5

        queue = deque()
        visited = [[0 for _ in range(n)] for _ in range(n)]

        # 시작점 위치
        nxt_x, nxt_y = ax + dx[s], ay + dy[s]
        queue.append((nxt_x, nxt_y, power-1))
        visited[nxt_x][nxt_y] = 1
        pre_cool_map[nxt_x][nxt_y] += power

        while queue:
            x, y, cur_power = queue.popleft()
            if cur_power == 0:
                continue

            # 다음 진행방향 체크
            if check_available(x, y, s):
                nxt_x, nxt_y = x + dx[s], y + dy[s]
                queue.append((nxt_x, nxt_y, cur_power-1))
                pre_cool_map[nxt_x][nxt_y] += cur_power
                visited[nxt_x][nxt_y] = 1

            # 대각선 체크
            ls, rs = (s - 1) % 4, (s + 1) % 4

            # 좌측 대각선
            if check_available(x, y, ls):
                if check_available(x + dx[ls], y + dy[ls], s):
                    nxt_x, nxt_y = x + dx[ls] + dx[s], y + dy[ls] + dy[s]
                    queue.append((nxt_x, nxt_y, cur_power-1))
                    pre_cool_map[nxt_x][nxt_y] += cur_power
                    visited[nxt_x][nxt_y] = 1

            # 우측 대각선
            if check_available(x, y, rs):
                if check_available(x + dx[rs], y + dy[rs], s):
                    nxt_x, nxt_y = x + dx[rs] + dx[s], y + dy[rs] + dy[s]
                    queue.append((nxt_x, nxt_y, cur_power-1))
                    pre_cool_map[nxt_x][nxt_y] += cur_power
                    visited[nxt_x][nxt_y] = 1

    return


def spread():
    global cool_map

    new_cool_map = copy.deepcopy(cool_map)
    for x in range(n):
        for y in range(n):
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]

                if nx < 0 or nx >= n or ny < 0 or ny >= n:
                    continue
                # 벽을 두고 있는 경우
                elif (x, y, i) in wall:
                    continue
                elif cool_map[x][y] > cool_map[nx][ny]:
                    _diff = (cool_map[x][y] - cool_map[nx][ny]) // 4
                    new_cool_map[x][y] -= _diff
                    new_cool_map[nx][ny] += _diff

    cool_map = new_cool_map

    return


def remove():
    for (x, y) in loc_remove:
        if cool_map[x][y]:
            cool_map[x][y] -= 1

    return


def check():
    for (x, y) in target_loc:
        if cool_map[x][y] < k:
            return False

    return True


# 격자 크기 n, 벽의 개수 m, 원하는 시원함 정도 k
n, m, k = map(int, input().split())

map_lst = [list(map(int, input().split())) for _ in range(n)]
cool_map = [[0 for _ in range(n)] for _ in range(n)]

target_loc = set()
air_conditioner = set()
for x in range(n):
    for y in range(n):
        if map_lst[x][y] >=2:
            air_conditioner.add((x, y, map_lst[x][y]-2))
        elif map_lst[x][y] == 1:
            target_loc.add((x, y))

# 양 방향으로 벽이 있으면 진행 불가로 판단
wall = []
for _ in range(m):
    # s (0: 상, 1: 좌)
    _x, _y, s = map(int, input().split())

    # 위쪽에 벽
    if s == 0:
        wall.append((_x - 1, _y - 1, 1))
        wall.append((_x - 2, _y - 1, 3))
    # 좌측에 벽
    elif s == 1:
        wall.append((_x - 1, _y - 1, 0))
        wall.append((_x - 1, _y - 2, 2))

# remove할 좌표들을 pre-define
loc_remove = set()

tmp_loc = [(0, i) for i in range(n)] + [(i, 0) for i in range(n)] + [(n-1, i) for i in range(n)] + [(i, n-1) for i in range(n)]
loc_remove.update(tmp_loc)

# 좌,상,우,하
dx = [0, -1, 0, 1]
dy = [-1, 0, 1, 0]

# 에어컨에 의해 냉방되는 map을 미리 만들어 둠
move()

answer = 0
while True:
    answer += 1

    for x in range(n):
        for y in range(n):
            cool_map[x][y] += pre_cool_map[x][y]

    spread()

    remove()

    if check():
        break
    elif answer >= 100:
        answer = -1
        break

print(answer)
