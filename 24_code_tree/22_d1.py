'''
start : 20:45
end : 22:44

회고 :
    - 미리 설계를 해두고 시작하면 좋다
    - 복잡도가 너무 높은 것 같아도 미리 연산량을 계산해보면 얼마 안 될 경우도 있다
    - 들어갈 basecamp 찾는 방식에서 갈 수 있는 모든 곳들을 찾아 두고 sort해야 함!!! -> 어떻게 할 지 다시 판단해보기
    
    - 현재 로직에서는 사람 움직일 위치를 찾기 위해 한 칸 이동점부터 시작해서 bfs (총 4번), add_people하기 위해 bfs (총 1번)
        - 해설 기준으로는 전체 map에 대해서 bfs 돌리고, 이후 for문 돌리면서 basecamp 위치 찾음 + 상하좌우 보면서 가장 작은 곳으로 움직임
        - 4번 대비 전체 맵 대상으로 도는게 나은 것 같고, basecamp는 sort 하는게 효율적인 듯
        - 다만, 종료 조건이 갈리는 경우에는 bfs 함수를 공통되게 만드는 것이 오히려 불편함


m명의 사람 , nxn 격자
m번 사람은 m분에 베이스캠프를 출발 -> 편의점으로 이동
모든 사람들의 목표 편의점은 다름

1. 본인이 가고 싶은 편의점 방향을 향해서 1칸 움직임
    - 최단거리, '상 좌 우 하' 순서의 우선 순위
2. 편의점 도착 시 멈춤
    - 이때부터 다른 사람들은 해당 편의점이 있는 칸을 지날 수 없음
    - 격자에 있는 사람들이 모두 이동한 후에 움직일 수 없는 칸이 됨
3. 현대 시간이 t분, t<=m이라면, 
    - t번 사람은 자신이 가고 싶은 편의점과 가장 가까운 베이스캠프에 들어감
    - 행이 작은 >> 열이 작은 베이스 캠프가 우선 순위
    - 해당 베이스 캠프는 지날 수 없는 칸이 됨

사람의 움직임 -> 해당 방향 넣고 bfs 돌려서 가장 가까운 방향으로 움직임
들어갈 basecamp 찾는 방식 -> 타겟 편의점으로부터 bfs, 방향 우선순위는 유지
'''

import copy

from collections import deque

def bfs(queue, visited, exit_condition=0):
    if exit_condition != 0:
        tar_x, tar_y = target[exit_condition]
    else:
        loc = []
        distance = -1

    while queue:
        x, y = queue.popleft()

        # exit_condition == 0, 베이스 캠프를 만났다면 종료
        if exit_condition == 0:
            if distance != -1 and visited[x][y] > distance:
                loc.sort(key = lambda x: (x[0], x[1]))
                return loc[0]

            if map_lst[x][y] == 1:
                if distance == -1 :
                    distance = visited[x][y]

                loc.append((x, y))

        # exit_condition != 0, 편의점을 만났다면 종료
        else:
            if (x, y) == (tar_x, tar_y):
                return visited[x][y]

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            elif map_lst[nx][ny] == -1:
                continue
            elif visited[nx][ny] != -1:
                continue

            queue.append((nx, ny))
            visited[nx][ny] = visited[x][y] + 1

    if exit_condition == 0:
        loc.sort(key=lambda x: (x[0], x[1]))
        return loc[0]

    return -1


def move(id, loc):
    x, y = loc

    visited = [[-1 for _ in range(n)] for _ in range(n)]
    visited[x][y] = 0

    # dir, distance
    d, min_distance = -1, -1
    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]

        if nx < 0 or nx >= n or ny < 0 or ny >= n:
            continue
        elif map_lst[nx][ny] == -1:
            continue
        elif visited[nx][ny] != -1:
            continue

        # visited 복사
        tmp_visited = copy.deepcopy(visited)
        tmp_visited[nx][ny] = tmp_visited[x][y] + 1

        queue = deque()
        queue.append((nx, ny))
        distance = bfs(queue, tmp_visited, exit_condition=id)

        if distance == -1:
            continue
        elif min_distance == -1:
            d = i
            min_distance = distance
        elif distance < min_distance:
            d = i
            min_distance = distance

    people[id] = (x + dx[d], y + dy[d])

    return


def check_loc():
    global people

    new_people = dict()
    for idx, loc in people.items():
        tar_x, tar_y = target[idx]

        # 편의점 도착했으면 삭제
        if (tar_x, tar_y) == loc:
            map_lst[tar_x][tar_y] = -1
        else:
            new_people[idx] = loc

    people = new_people

    return


def add_people(time):
    queue = deque()

    _x, _y = target[time]
    queue.append((_x, _y))

    visited = [[-1 for _ in range(n)] for _ in range(n)]
    visited[_x][_y] = 0

    # 가장 가까운 베이스캠프 찾기
    (x, y) = bfs(queue, visited, exit_condition=0)

    map_lst[x][y] = -1
    people[time] = (x, y)

    return


n, m = map(int, input().split())

# 상 좌 우 하
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

# 0: 빈 칸, 1: 베이스 캠프
map_lst = [list(map(int, input().split())) for _ in range(n)]

# 가고 싶은 편의점 정보
target = dict()
for i in range(1, m + 1):
    x, y = map(int, input().split())
    target[i] = (x - 1, y - 1)

people = dict()

t = 0
while t <= m or people:
    t += 1

    if people:
        # 사람 움직임
        for id, loc in people.items():
            move(id, loc)

        # 편의점 도착 판단
        check_loc()

    if t <= m:
        add_people(t)

print(t)