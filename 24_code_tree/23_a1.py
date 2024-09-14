def check_debug():
    check_map = [[0 for _ in range(M)] for _ in range(N)]
    for x in range(N):
        for y in range(M):
            if map_lst[x][y]:
                check_map[x][y] = map_lst[x][y][0].damage
            else:
                check_map[x][y] = 0

    for i in check_map:
        print(i)

    return


'''
걸린 시간 : 2 + 1.5 = 3.5시간
회고 : 
    - class로 만드는 게 map 전체를 한 번에 확인해야 할 때에는 어려움
        - 우선순위 비교라고 하더라도 class 없이 하게끔 해야 할 듯
    - 종료 조건에 있어서 연산을 한 뒤에 break가 걸리는 경우 식별하지 못함
    - 마찬가지로 그 즉시 종료라는 조건을 놓침
    
    - 정렬을 할 때, key로 class의 값을 줄 수 있음
        - tower.sort(key=lambda:(x.damage, -x.attack_time, -(x.x+x.y), x.y)
    - 경로를 역추적할 때, 어느 위치에서 옮겨왔는지 좌표를 저장하는 map을 만들어서 추적할 수 있음
        - 도착지점에서부터 거꾸로 오는 거랑 다를 바는 없는 듯, 다만 (전체 bfs 도는 시간 vs 메모리 더 쓰는 방식) 차이

NxM 격자, 모든 위치에는 포탑 존재
포탑에는 공격력 존재, 공격력이 0 이하가 된 포탑은 파괴

K번의 턴, 4가지 액션 순서대로 수행
부서지지 않은 포탑이 1개가 되면, 수행 중지

1. 공격자 선정
    - 가장 약한 포탑이 공격자로 선정
    - 해당 포탑은 N+M만큼 공격력 증가
        - 공격력이 낮은 >> 가장 최근에 공격한 포탑 >> 행+열이 큰 >> 열이 큰
2. 공격
    - 자신을 제외한 가장 강한 포탑을 공격
        - 공격력이 높은 >> 공격한 지 오래된 >> 행+열이 작은 >> 열이 작은
    - 레이저 공격 먼저 시도 >> 포탄 공격
        - 레이저 공격 :
            - 공격자의 위치에서 최단 경로로 공격 가능할 시 시도
            - 우/하/좌/상의 우선순위
            - 부서진 포탑의 위치는 지날 수 없음
            - 반대편으로 나오는 무빙 가능 (%연산자로 계산)
            - 해당 포탑은 공격력만큼 감소, 경로에 있는 포탑은 절반만큼 (//)
        - 포탄 공격
            - 공격자 공격력 만큼의 피해
            - 주변 8칸에 대해서는 절반만큼 피해 (//)
            - 공격자는 공격에 영향을 받지 않음
            - 가장자리의 경우, 레이저 공격처럼 반대편 격자에 영향 존재
3. 포탑 부서짐
    - 공격력이 0 이하인 포탑이 부서짐
4. 포탑 정비
    - 부서지지 않은 포탑 중 공격과 무관한 포탑은 공격력이 1씩 증가


bfs를 target에서부터 돌리고, 시작 위치에서부터 타겟까지 진행하는 방식으로 수행
3 2 3 4
2 1 - 5
1 0 - 6
2 1 - 5
3 2 3 4

5 4 3 2
6 5 - 1
7 6 - 0
6 5 - 1
5 4 3 2

'''

from collections import deque

class tower:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self.attack_time = 0

    def __gt__(self, other):
        # 공격자 선정 (공격력이 높은 >> 공격한 지 오래된 >> 행+열이 작은 >> 열이 작은)
        if self.damage != other.damage:
            return self.damage > other.damage
        elif self.attack_time != other.attack_time:
            return self.attack_time < other.attack_time
        elif (self.x + self.y) != (other.x + other.y):
            return (self.x + self.y) < (other.x + other.y)
        elif self.y != other.y:
            return self.y < other.y

    def __lt__(self, other):
        # 피 공격자 선정 (공격력이 낮은 >> 가장 최근에 공격한 포탑 >> 행+열이 큰 >> 열이 큰)
        if self.damage != other.damage:
            return self.damage < other.damage
        elif self.attack_time != other.attack_time:
            return self.attack_time > other.attack_time
        elif (self.x + self.y) != (other.x + other.y):
            return (self.x + self.y) > (other.x + other.y)
        elif self.y != other.y:
            return self.y > other.y

    def print_status(self):
        print(f'self.x : {self.x}')
        print(f'self.y : {self.y}')
        print(f'self.damage : {self.damage}')
        print(f'self.attack_time : {self.attack_time}')


def choose():
    attacker = tower(-1, -1, -1)
    target = tower(-1, -1, -1)

    for x in range(N):
        for y in range(M):
            if not map_lst[x][y]:
                continue

            tmp = map_lst[x][y][0]

            # 공격자 선정 : 비교군이 없거나 우선순위가 더 높은
            if (attacker.damage == -1) or (tmp < attacker):
                attacker = tmp

            # 피 공격자 선정 : 비교군이 없거나 우선순위가 더 높은
            if (target.damage == -1) or (tmp > target):
                target = tmp

    attacker.damage += (N + M)
    attacker.attack_time = k

    return attacker, target


def bfs(queue):
    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx = (x + dx[i]) % N
            ny = (y + dy[i]) % M

            # 넘어감
            if visited[nx][ny] != -1:
                continue
            elif not map_lst[nx][ny]:
                continue

            queue.append((nx, ny))
            visited[nx][ny] = visited[x][y] + 1

    return


def attack():
    tx, ty = target.x, target.y

    queue = deque()
    queue.append((tx, ty))
    visited[tx][ty] = 0
    bfs(queue)

    # 최단 경로가 있는지 확인
    x, y = attacker.x, attacker.y
    attack_map[x][y] = 1

    # 레이저 공격
    if visited[x][y] != -1:
        for _ in range(visited[x][y]):
            for i in range(4):
                nx = (x + dx[i]) % N
                ny = (y + dy[i]) % M

                if visited[nx][ny] != visited[x][y] -1:
                    continue

                # 공격 -> 중도는 절반 데미지, 목적지는 풀 데미지
                if (nx, ny) != (tx, ty):
                    map_lst[nx][ny][0].damage -= (attacker.damage // 2)
                else:
                    map_lst[nx][ny][0].damage -= attacker.damage
                
                # 공격력 0 이하면 파괴
                if map_lst[nx][ny][0].damage <= 0:
                    map_lst[nx][ny] = []

                # 실제 공격 여부 체크 위해서
                attack_map[nx][ny] = 1
                x, y = nx, ny
                break
    # 포탄 공격
    else:
        for i in range(9):
            nx = (tx + dx_all[i]) % N
            ny = (ty + dy_all[i]) % M

            # 공격자 본인일 경우
            if (nx, ny) == (x, y):
                continue
            elif not map_lst[nx][ny]:
                continue

            # 공격 -> 중도는 절반 데미지, 목적지는 풀 데미지
            if (nx, ny) != (tx, ty):
                map_lst[nx][ny][0].damage -= (attacker.damage // 2)
            else:
                map_lst[nx][ny][0].damage -= attacker.damage

            # 공격력 0 이하면 파괴
            if map_lst[nx][ny][0].damage <= 0:
                map_lst[nx][ny] = []

            attack_map[nx][ny] = 1

    return


def heal():
    for x in range(N):
        for y in range(M):
            if not map_lst[x][y]:
                continue
            elif attack_map[x][y]:
                continue

            map_lst[x][y][0].damage += 1

    return


N, M, K = map(int, input().split())

# 빈 곳은 부서진 포탑 위치
map_lst = [[[] for _ in range(M)] for _ in range(N)]

for n in range(N):
    tmp = list(map(int, input().split()))
    for m, val in enumerate(tmp):
        if val == 0:
            continue

        map_lst[n][m].append(tower(n, m, val))

# 우 하 좌 상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

dx_all = [0, 0, 1, 1, 1, 0, -1, -1, -1]
dy_all = [0, 1, 1, 0, -1, -1, -1, 0, 1]

for k in range(1, K+1):
    visited = [[-1 for _ in range(M)] for _ in range(N)]
    attack_map = [[0 for _ in range(M)] for _ in range(N)]
    attacker, target = choose()

    # 포탑이 한 개만 남으면 종료
    if attacker == target:
        attacker.damage -= (N+M)
        break

    attack()

    # 포탑이 한 개만 남으면 종료
    if attacker == target:
        attacker.damage -= (N+M)
        break
    heal()

answer = 0
for x in range(N):
    for y in range(M):
        if not map_lst[x][y]:
            continue

        answer = max(answer, map_lst[x][y][0].damage)

print(answer)
