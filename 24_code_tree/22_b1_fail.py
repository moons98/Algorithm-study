def print_map():
    for i in map_lst:
        print(i)

'''
start : 20:05
end : 23:40


회고 :
    - circular queue로는 못 풀었을까?
    - 꽉 찬 원에서 도는 경우 해결 못함

    - 해설의 경우, 
        - dfs로 각 팀의 동선이 저장됨, 0번 위치가 head
        - tail은 따로 list 만들어 관리
        - 각 위치가 어떤 팀의 동선인지 관리하는 map이 존재
        - list.index()로 순서를 찾음


nxn 격자, 꼬리 잡기 놀이
머리 사람과 꼬리 사람이 존재, 주어진 이동 선을 따라서만 이동

1. 머리 사람을 따라서 한 칸 이동
2. 각 라운드마다 정해진 선을 따라 공이 던져짐
    - 4n번째 라운드를 넘어 가는 경우에는 다시 1번째 라운드의 방향으로 돌아감
3. 해당 선에 사람이 있으면 최초에 만나는 사람이 공을 얻어 점수를 얻음
    - 머리 사람을 기준으로 k번째 사람이라면, k**2만큼 점수를 얻음
    - 공을 획득한 팀은 머리 사람과 꼬리 사람이 바뀜

0은 빈칸,
1은 머리 사람,
2는 나머지,
3은 꼬리 사람
4는 이동선

각 팀이 획득한 점수의 '총합'을 구하는 프로그램 작성

각 팀의 머리 사람과 꼬리 사람의 좌표를 저장
공을 맞으면 해당 위치부터 bfs해서 1을 만날때까지 cnt, 이후 1번과 3번의 위치를 바꾸기

'''

import copy
from collections import deque


def bfs():
    global queue, visited, group

    while queue:
        x, y = queue.popleft()

        # 머리, 꼬리인지 확인
        if map_lst[x][y] == 1:
            head = (x, y)
        elif map_lst[x][y] == 3:
            tail = (x, y)

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            # 지날 수 없는 좌표
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            # 이미 지난 위치
            elif visited[nx][ny]:
                continue
            # 빈칸
            elif map_lst[nx][ny] == 0:
                continue

            visited[nx][ny] = 4
            queue.append((nx, ny))

    group[head] = tail

    return


def move_group():
    global group, map_lst

    new_group = dict()
    new_map = copy.deepcopy(visited)

    queue = deque()
    for (_head, _tail) in group.items():
        (x, y) = _head

        # 한 루프에 지금 포인트가 움직일 위치만 찾으면 됨
        # tail 위치에 도달하면 break
        head_tmp = dict()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            # 지날 수 없는 좌표
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            elif map_lst[nx][ny] == 0:
                continue

            head_tmp[map_lst[nx][ny]] = (nx, ny)

        if 4 in head_tmp.keys():
            new_head = head_tmp[4]
            # tail 결정됨
            if 3 in head_tmp.keys():
                new_tail = head_tmp[3]
                new_map[_head[0]][_head[1]] = 3
            else:
                map_lst[_head[0]][_head[1]] = 5
                queue.append(_head)
        elif 3 in head_tmp.keys():
            new_head = head_tmp[3]
            map_lst[_head[0]][_head[1]] = 5
            queue.append(_head)

        new_map[new_head[0]][new_head[1]] = 1


        while queue:
            x, y = queue.popleft()
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]

                # 지날 수 없는 좌표
                if nx < 0 or nx >= n or ny < 0 or ny >= n:
                    continue
                elif map_lst[nx][ny] == 0:
                    continue

                if map_lst[nx][ny] == 2:
                    new_map[x][y] = 2
                    map_lst[nx][ny] = 5
                    queue.append((nx, ny))
                # 다음 위치가 3인 경우, 4로 현재 위치를 바꿔 줘야 함
                elif map_lst[nx][ny] == 3:
                    new_map[x][y] = 3
                    new_tail = (x, y)

        new_group[new_head] = new_tail

    group = new_group
    map_lst = new_map

    return


def throw_ball(start_loc, d):
    global answer, group

    x, y = start_loc

    x -= dx[d]
    y -= dy[d]
    while True:
        x += dx[d]
        y += dy[d]

        # 지날 수 없는 좌표
        if x < 0 or x >= n or y < 0 or y >= n:
            return 0, (-1, -1)

        if map_lst[x][y] == 1:
            return 1, (x, y)
        elif map_lst[x][y] == 2 or map_lst[x][y] == 3:
            target = (x, y)
            break

    # cal score
    queue = deque()
    queue.append(target)

    cnt = [[0 for _ in range(n)] for _ in range(n)]
    cnt[target[0]][target[1]] = 1
    while queue:
        x, y = queue.popleft()

        for i in range(4):
            nx, ny  = x + dx[i], y + dy[i]

            # 지날 수 없는 좌표
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            elif map_lst[nx][ny] == 0 or map_lst[nx][ny] == 4:
                continue
            elif cnt[nx][ny] != 0:
                continue

            if map_lst[nx][ny] == 1:
                return (cnt[x][y] + 1) ** 2, (nx, ny)
            elif map_lst[nx][ny] == 2 or map_lst[nx][ny] == 3:
                cnt[nx][ny] = cnt[x][y] + 1
                queue.append((nx, ny))

    return


# 격자 크기, 팀의 개수, 라운드 수
n, m, k = map(int, input().split())

map_lst = [list(map(int, input().split())) for _ in range(n)]

# 우 상 좌 하
dx = [0, -1, 0, 1]
dy = [1, 0, -1, 0]

group = dict()

# bfs 돌아서 모든 그룹의 머리와 꼬리 위치 찾기
# visited는 이제 갈 수 있는 길이 됨
visited = [[0 for _ in range(n)] for _ in range(n)]
queue = deque()
for x in range(n):
    for y in range(n):
        if map_lst[x][y] == 0:
            continue
        if not visited[x][y]:
            visited[x][y] = 4
            queue.append((x,y))
            bfs()

answer = 0
for i in range(k):
    # 공이 던져지는 시작점과 방향 계산, 4n마다 반복
    # 짝수면 가로로 진행, 홀수면 세로로 진행
    _tmp = i % (4 * n)
    _a = _tmp // n
    _b = _tmp % n

    if _a == 0:
        _loc = (_b, 0)
    elif _a == 1:
        _loc = (n-1, _b)
    elif _a == 2:
        _loc = (n-1 - _b, n-1)
    elif _a == 3:
        _loc = (0, n-1 - _b)

    move_group()
    score, head_loc = throw_ball(_loc, _a)

    if head_loc in group.keys():
        tail = group.pop(head_loc)
        group[tail] = head_loc

        map_lst[head_loc[0]][head_loc[1]] = 3
        map_lst[tail[0]][tail[1]] = 1

    answer += score
 

print(answer)


'''
7 2 1
2 2 1 0 0 0 0
2 0 3 0 2 1 4
2 2 2 0 2 0 4
0 0 0 0 3 0 4
0 0 4 4 4 0 4
0 0 4 0 0 0 4
0 0 4 4 4 4 4

7 2 1
4 4 1 0 0 0 0
4 0 3 0 2 1 4
4 4 4 0 2 0 4
0 0 0 0 3 0 4
0 0 4 4 4 0 4
0 0 4 0 0 0 4
0 0 4 4 4 4 4

7 3 5
3 2 1 0 0 0 0
4 0 4 0 2 1 4
4 4 4 0 2 0 4
0 0 0 0 3 4 4
2 1 3 2 0 0 0
2 0 0 2 0 0 0
2 2 2 2 0 0 0

7 2 900
1 3 2 0 0 0 0
2 0 2 0 2 1 4
2 2 2 0 2 0 4
0 0 0 0 3 0 4
0 0 4 4 4 0 4
0 0 4 0 0 0 4
0 0 4 4 4 4 4
'''






