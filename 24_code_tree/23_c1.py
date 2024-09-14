
'''
start : 20:15
end : 21:25

회고 :
    - 사라진 기사에게 명령을 내리면 동작이 없다는 조건을 놓침
    - 그 이외에는 한 칸씩만 움직이므로 미리 loc_set을 만들어두고 진행하면 쉬움

LxL 격자
좌상단 (1,1), 각 칸은 빈칸, 함정, 벽으로 구성

기사의 초기 위치는 (r,c), hxw 크기의 직사각형 형태, 각 기사의 체력은 k

1. 기사 이동
    - 상하좌우 중 한 칸으로 이동
    - 이동하려는 위치에 다른 기사가 있으면 연쇄적으로 밀려남
    - 움직일 수 없다면 모든 기사는 이동 불가
2. 대결 데미지
    - 밀려난 기사들은 피해 입음
    - 놓여 있는 함정의 수만큼 피해를 입음
    - 체력 이상의 데미지를 입을 경우 사라짐
    - 명령을 받은 기사는 피해 x
    - 기사는 모두 밀린 이후에 데미지를 입음
    - 밀려진 위치에 함정이 전혀 없다면 피해를 입지 않음

생존한 기사들이 총 받은 데미지의 합
'''
import copy

from collections import deque

def loc_set(r, c, h, w, d):
    # 상, 우, 하, 좌
    if d == 0:
        loc = deque([(r, c + i) for i in range(w)])
    elif d == 1:
        loc = deque([(r + i, c + w - 1) for i in range(h)])
    elif d == 2:
        loc = deque([(r + h - 1, c + i) for i in range(w)])
    elif d == 3:
        loc = deque([(r + i, c) for i in range(h)])

    return loc

def make_knight_map():
    global knight_map

    knight_map = [[0 for _ in range(L)] for _ in range(L)]
    for idx, (r, c, h, w, _) in knights.items():
        for x in range(r, r+h):
            for y in range(c, c+w):
                knight_map[x][y] = idx

    return


def dfs(queue):
    while queue:
        x, y = queue.popleft()
        nx, ny = x + dx[d], y + dy[d]

        # 지날 수 없거나 벽을 만나는 경우
        if nx < 0 or nx >= L or ny < 0 or ny >= L:
            return -1
        elif map_lst[nx][ny] == 2:
            return -1

        # 다른 기사가 위치한 칸일 경우
        if knight_map[nx][ny]:
            nxt_knight = knight_map[nx][ny]
            if nxt_knight in move_knight:
                continue
            
            # 움직인 기사에 등록
            move_knight.add(nxt_knight)
            
            # queue에 추가
            r, c, h, w, _ = knights[nxt_knight]
            queue += loc_set(r, c, h, w, d)

    return 1


def move(i, d):
    global move_knight, knights

    # 자기 자신 빼고, 움직인 기사 체크
    move_knight = set()

    # 기사 맵 갱신
    make_knight_map()

    r, c, h, w, _ = knights[i]
    queue = loc_set(r, c, h, w, d)

    flag = dfs(queue)
    if flag == -1:
        return

    # 움직인 기사들 갱신
    new_knights = copy.deepcopy(knights)

    # 자기 자신 갱신
    r, c, h, w, k = knights[i]
    new_knights[i] = (r+dx[d], c+dy[d], h, w, k)

    for idx in move_knight:
        r, c, h, w, k = knights[idx]

        r += dx[d]
        c += dy[d]

        # 받은 데미지 계산
        damage = 0
        for x in range(r, r+h):
            for y in range(c, c+w):
                if map_lst[x][y] == 1:
                    damage += 1
        
        # 데미지가 체력 이상, dict 갱신
        if k - damage <= 0:
            score[idx] = -1

            # 사라진 기사 빼줌
            new_knights.pop(idx)
            continue

        score[idx] += damage
        new_knights[idx] = (r, c, h, w, k-damage)

    knights = new_knights

    return



L, N, Q = map(int, input().split())

# 0: 빈칸, 1: 함정, 2: 벽
map_lst = [list(map(int, input().split())) for _ in range(L)]

knights = dict()
for idx in range(N):
    r, c, h, w, k = map(int, input().split())
    knights[idx + 1] = (r-1, c-1, h, w, k)

move_knight = set()

score = {i+1:0 for i in range(N)}

# 상, 우, 하, 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for _ in range(Q):
    i, d = map(int, input().split())

    if i not in knights.keys():
        continue

    move(i, d)

answer = [i for i in score.values() if i != -1]
print(sum(answer))










