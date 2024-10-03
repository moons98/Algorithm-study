'''
마법의 숲 탐색

start: 23:00
end: 24:10

회고
    - 푸는 시간은 확실히 빨라졌는데, 피곤해서 그런지 조건 놓치는 경우가 생김
    - 오늘은 등호 빼먹는 실수함 -> 이건 디버깅도 안될듯;;

        if nx >= R or ny < 0 or ny >= C:
            return 0
        elif nx >= 0 and map_lst[nx][ny]:
            return 0


- RxC 격자
- 숲의 동/서/남은 벽으로 막혀 있으며, 정령들은 북쪽을 통해서만 들어올 수 있음
- K명의 정령은 골렘을 타고 숲 탐색
- 골렘은 십자 모양의 구조를 가짐, 한 칸은 골렘의 출구

1. 남쪽으로 한 칸 내려감
2. 이동 불가 시, 서쪽으로 회전 + 남쪽으로 내려감
3. 이동 불가 시, 동쪽으로 회전 + 남쪽으로 내려감
4. 골렘이 더 이상 이동할 수 없으면 정령은 인접 칸으로 이동
    - 골렘의 출구가 다른 골렘과 인접하고 있다면 해당 출구를 통해 다른 골렘으로 이동 가능
    - 갈 수 있는 모든 칸 중 가장 남쪽의 칸으로 이동
    - 해당 위치가 최종 위치
    - 각 정령이 도달하는 최종 위치를 누적

- 골렘이 최대한 남쪽으로 이동했음에도 여전히 몸의 일부가 숲을 벗어난 상태라면, map을 reset


'''

from collections import deque

def move_down(x, y):
    # check_idx: [1,2,3]
    for i in [1,2,3]:
        nx, ny = x + dx[i], y + dy[i]
        if nx >= R or ny < 0 or ny >= C:
            return 0
        elif nx >= 0 and map_lst[nx][ny]:
            return 0

    return 1


def move_left(x, y):
    # check_idx: [0,2,3]
    for i in [0,2,3]:
        nx, ny = x + dx[i], y + dy[i]
        if nx >= R or ny < 0 or ny >= C:
            return 0
        elif nx >= 0 and map_lst[nx][ny]:
            return 0

    return 1


def move_right(x, y):
    # check_idx: [0,1,2]
    for i in [0,1,2]:
        nx, ny = x + dx[i], y + dy[i]
        if nx >= R or ny < 0 or ny >= C:
            return 0
        elif nx >= 0 and map_lst[nx][ny]:
            return 0


    return 1

def bfs(queue):
    while queue:
        (x, y) = queue.popleft()

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            if nx < 0 or nx >= R or ny < 0 or ny >= C:
                continue
            elif visited[nx][ny]:
                continue
            elif not map_lst[nx][ny]:
                continue

            # 같은 숫자거나 지금 위치가 출구
            if (map_lst[nx][ny] == map_lst[x][y]) or (map_lst[nx][ny] == -map_lst[x][y]) or (map_lst[x][y] < 0):
                visited[nx][ny] = 1
                queue.append((nx, ny))

    return


def find_loc(x, y, d):
    global map_lst, visited
    
    # 해당 로봇의 위치 채우기
    if x < 1:
        map_lst = [[0 for _ in range(C)] for _ in range(R)]
        return 0
    else:
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            map_lst[nx][ny] = idx

        # 중앙, 출구 표시
        map_lst[x][y] = idx
        map_lst[x + dx[d]][y + dy[d]] = -idx

    # 가장 아래까지 도달할 수 있는 위치 찾기
    visited = [[0 for _ in range(C)] for _ in range(R)]
    queue = deque()

    queue.append((x, y))
    visited[x][y] = 1
    bfs(queue)

    for x in range(R-1, -1, -1):
        for y in range(C):
            if visited[x][y]:
                return x

    return


R, C, K = map(int, input().split())

map_lst = [[0 for _ in range(C)] for _ in range(R)]

#  골렘이 출발하는 열 c, 골렘의 출구 방향 정보 d
robots = dict()
for k in range(1, K+1):
    c, d = map(int, input().split())
    robots[k] = (c-1, d)

# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

answer = []
for idx, (c, d) in robots.items():
    sx, sy = (-2, c)

    # 더 이상 움직이지 못할 때까지 움직임
    while True:
        if move_down(sx+1, sy):
            sx += 1
        elif move_left(sx, sy-1) and move_down(sx+1, sy-1):
            sx += 1
            sy -= 1
            d = (d - 1) % 4
        elif move_right(sx, sy+1) and move_down(sx+1, sy+1):
            sx += 1
            sy += 1
            d = (d + 1) % 4
        else:
            break

    cur_answer = find_loc(sx, sy, d)
    if cur_answer:
        answer.append(cur_answer + 1)
    
print(sum(answer))
