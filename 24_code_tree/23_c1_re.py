
'''
왕실의 기사 대결

회고 :
    - 움직인 기사를 관리할 때, set을 사용하지 않으면, 두 칸을 움직이는 경우가 생길 수 있음 !!!

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
from collections import deque

def make_map():
    global knight_map

    knight_map = [[0 for _ in range(L)] for _ in range(L)]
    for i, (r, c, h, w, k) in knight.items():
        for x in range(r, r+h):
            for y in range(c, c+w):
                knight_map[x][y] = i

    return


def find_loc(i, d):
    r, c, h, w, k = knight[i]

    # 상 우 하 좌
    if d == 0:
        loc = [(r, c+j) for j in range(w)]
    elif d == 1:
        loc = [(r+j, c+w-1) for j in range(h)]
    elif d == 2:
        loc = [(r+h-1, c+j) for j in range(w)]
    elif d == 3:
        loc = [(r+j, c) for j in range(h)]

    return deque(loc)


def move(i, d):
    # 만약 없어진 기사라면 pass
    if i not in knight.keys():
        return 

    # 움직인 기사 관리
    moved_knights = set()
    moved_knights.add(i)

    queue = find_loc(i, d)

    while queue:
        x, y = queue.popleft()
        
        # 움직일 위치
        nx, ny = x + dx[d], y + dy[d]

        # 벽을 만나거나 밖으로 나가면 종료
        if nx < 0 or nx >= L or ny < 0 or ny >= L:
            return
        elif trap_map[nx][ny] == 2:
            return
        # 다른 기사를 만나면 queue에 추가
        elif knight_map[nx][ny]:
            nxt = knight_map[nx][ny]
            queue += find_loc(nxt, d)
            moved_knights.add(nxt)

    # 기사 정보 업데이트
    for _knight in moved_knights:
        r, c, h, w, k = knight.pop(_knight)

        nr, nc = r + dx[d], c + dy[d]

        # 자기 자신은 데미지 입지 않음
        if i == _knight:
            knight[_knight] = (nr, nc, h, w, k)
            continue

        # 점수 계산
        damage = 0
        for x in range(nr, nr+h):
            for y in range(nc, nc+w):
                if trap_map[x][y] == 1:
                    damage += 1

        nk = max(0, k-damage)

        # 생존하면, score 갱신
        if nk:
            score[_knight] += damage
            knight[_knight] = (nr, nc, h, w, nk)
        else:
            score[_knight] = -1

    return


L, N, Q = map(int, input().split())

trap_map = [list(map(int, input().split())) for _ in range(L)]

knight = dict()
for i in range(1, N+1):
    r, c, h, w, k = map(int, input().split())
    knight[i] = (r-1, c-1, h, w, k)

# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 죽은 기사는 -1 처리
score = [0 for _ in range(N+1)]

# 메인 라운드 진행
for _ in range(Q):
    # 기사 맵 갱신
    make_map()

    i, d = map(int, input().split())
    move(i, d)

tmp = [i for i in score if i != -1]
print(sum(tmp))