
'''
마법의 숲 탐색

start : 23:20
end : 24:50


회고 :
    - 재귀적으로 함수 돌 때, 가장 안쪽 iteration에서만 내가 원하는 값이 나옴
    - global 변수를 사용해서 그 값만 빼놓기


- RxC 격자
- 숲의 북쪽으로만 정령이 들어올 수 있음, 나머지는 막혀 있음

- K명의 정령은 골렘을 타고 숲 탐색
- 골렘의 중앙을 제외한 4칸 중 한 칸은 골렘의 출구
- 어느 방향에서든 탑승 가능, 내릴 때에는 정해진 출구로만 가능

- 골렘의 중앙이 c열이 되도록 하는 위치에서 내려오기 시작, 출구는 d 방향

1. 남쪽으로 한 칸 내려감
2. 이동할 수 없으면 서쪽 방향으로 회전하면서 내려감
    - 서쪽으로 한 칸 + 출구가 반시계로 90도 회전, 남쪽으로 진행
3. 이동할 수 없으면 동쪽 방향으로 회전하면서 진행
    - 동쪽으로 한 칸 + 출구가 시계로 90도 회전, 남쪽으로 진행

- 골렘이 가장 남족에 도달하면 정령은 골렘 내에서 인접 칸으로 이동 가능
- 출구가 다른 골렘과 이어져 있다면 이동 가능
- 갈 수 있는 모든 칸 중 가장 남쪽의 칸으로 이동하고 이동을 완전히 종료

- 만약 골렘이 최재한 남쪽으로 이동했지만 몸 일부가 여전히 숲을 벗어난다면 전체 맵을 비우고 다시 진행

정령의 최종 위치의 행 번호의 합 출력
'''

from collections import deque

def go_down(x, y):
    # 남쪽 이동 시, 중심점
    cx, cy = x + dx[2], y + dy[2]

    # 중심점 기준으로 (우, 하, 좌) 좌표 확인
    # 행이 0보다 작은 경우는 신경 쓰지 않음
    for i in [1, 2, 3]:
        nx, ny = cx + dx[i], cy + dy[i]
        
        if nx < 0:
            continue
        # 양 날개가 격자를 벗어남
        elif ny < 0 or ny >= C:
            return 0
        # 다른 골렘이 위치
        elif map_lst[nx][ny]:
            return 0

    return 1


def go_left(x, y):
    # 서쪽 이동 시, 중심점
    cx, cy = x + dx[3], y + dy[3]

    # 중심점 기준으로 (상, 하, 좌) 좌표 확인
    # 행이 0보다 작은 경우는 신경 쓰지 않음
    for i in [0, 2, 3]:
        nx, ny = cx + dx[i], cy + dy[i]

        if nx < 0:
            continue
        # 양 날개가 격자를 벗어남
        elif ny < 0 or ny >= C:
            return 0
        # 다른 골렘이 위치
        elif map_lst[nx][ny]:
            return 0

    return 1

def go_right(x, y):
    # 동쪽 이동 시, 중심점
    cx, cy = x + dx[1], y + dy[1]

    # 중심점 기준으로 (상, 우, 하) 좌표 확인
    # 행이 0보다 작은 경우는 신경 쓰지 않음
    for i in [0, 1, 2]:
        nx, ny = cx + dx[i], cy + dy[i]

        if nx < 0:
            continue
        # 양 날개가 격자를 벗어남
        elif ny < 0 or ny >= C:
            return 0
        # 다른 골렘이 위치
        elif map_lst[nx][ny]:
            return 0

    return 1


def move(x, y, d):
    global final_loc

    # 남쪽으로 우선 진행
    if go_down(x, y):
        x += 1
    else:
        # 서쪽 진행 + 남쪽 진행
        if go_left(x, y) and go_down(x, y-1):
            x += 1
            y -= 1
            d = (d - 1) % 4
        # 동쪽 진행 + 남쪽 진행
        elif go_right(x, y) and go_down(x, y+1):
            x += 1
            y += 1
            d = (d + 1) % 4
        # 더이상 진행 불가능
        else:
            final_loc = (x, y, d)
            return

    # 가장 아래 행에 도달했는지 확인
    if x == R-2:
        final_loc = (x, y, d)
        return

    # 재귀적으로 이동
    move(x, y, d)

    return


def bfs(x, y):
    visited = [[0 for _ in range(C)] for _ in range(R)]
    visited[x][y] = 1

    queue = deque()
    queue.append((x, y))
    while queue:
        x, y = queue.popleft()

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            if nx < 0 or nx >= R or ny < 0 or ny >= C:
                continue
            elif visited[nx][ny]:
                continue

            # 같은 숫자이거나 현재 골렘의 출구인 경우
            if (map_lst[nx][ny] == map_lst[x][y]) or (map_lst[nx][ny] == -map_lst[x][y]):
                queue.append((nx, ny))
                visited[nx][ny] = 1
            # 현재 칸이 출구 칸일 경우, 어떤 골렘으로도 이동 가능
            elif (map_lst[x][y] < 0) and map_lst[nx][ny]:
                queue.append((nx, ny))
                visited[nx][ny] = 1

    # 가장 큰 행 찾기
    for x in range(R-1, 0, -1):
        for y in range(C):
            if visited[x][y]:
                return x

    return



R, C, K = map(int, input().split())

# (출발하는 열 c, 출구 방향 d)
robot = dict()
for k in range(1, K+1):
    c, d = map(int, input().split())
    robot[k] = [c-1, d]

# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

map_lst = [[0 for _ in range(C)] for _ in range(R)]

answer = []
for k in range(1, K+1):
    c, d = robot[k]

    # 출발 위치의 중심점은 (-2, c-1)
    move(-2, c, d)
    (tx, ty, d) = final_loc

    # 최종 값이 격자 밖인 경우 맵 리셋
    if (tx-1) < 0:
        map_lst = [[0 for _ in range(C)] for _ in range(R)]
        continue

    # 맵 채우기
    for i in range(4):
        nx, ny = tx + dx[i], ty + dy[i]
        map_lst[nx][ny] = k

    # 중심과 출구 표시
    map_lst[tx][ty] = k
    map_lst[tx + dx[d]][ty + dy[d]] = -k

    # 가장 행이 큰 곳으로 움직임, append value for debugging
    cur_answer = bfs(tx, ty)
    answer.append(cur_answer + 1)

print(sum(answer))
