'''
포탑 부수기

start: 11:30
end: 13:20

회고 :
    - class를 만드는 게 훨씬 편함
    - 여러개 변수 만들어서 접근하는게 indexing 측면에서도 비효율적 (340ms -> 410ms)
    - 변수 관리도 힘듦


- NxM 격자
- 각 포탑에는 공격력 존재, 0 이하가 된다면 파괴
- 최초에 부서진 포탑이 존재할 수 있음

- 부서지지 않은 포탑이 1개가 된다면 그 즉시 종료

1. 공격자 선정
    - 부서지지 않은 포탑 중 가장 약한 포탑이 공격자로 선정
    - N+M 만큼 공격력 증가
    - 공격력이 가장 낮은 >> 가장 최근에 공격한 포탑 >> 행+열이 가장 큰 >> 열이 큰

2. 공격자의 공격
    - 자신을 제외한 가장 강한 포탑 공격
    - 공격력이 가장 높은 >> 공격한지 가장 오래된 >> 행+열이 가장 작은 >> 열이 작은
    - 레이저 공격 >> 포탄 공격으로 시도

    (1) 레이저 공격
        - 상하좌우 4개 방향으로 움직일 수 있음
        - 부서진 포탑이 있는 위치 는 지날 수 없음
        - 가장자리에서 막힌 방향으로 진행하면 반대로 나옴
        - 레이저 공격은 최단 거리로 진행, 경로 없으면 포탄 공격 진행
        - 우선순위는 우,하,좌,상 순서
        - 공격 대상은 공격력만큼, 경로에 있는 포탑은 공격력//2 만큼 공격 받음

    (2) 포탄 공격
        - 공격 대상에 포탄 발사, 공격 대상은 공격력만큼, 주변 포탑은 공격력//2 만큼 데미지
        - 공격자는 영향 받지 않음
        - 반대편 격자에 피해 미침

3. 포탑 부서짐
    - 공격력이 0 이하인 포탑은 파괴

4. 포탑 정비
    - 공격과 무관한 포탑은 공격력이 1씩 증가

남아 있는 포탑 중 가장 강한 포탑의 공격력 출력

- bfs로 경로가 있는지 먼저 확인
- 다음 진행 방향을 확인하기 위해 도착지부터 거꾸로 진행해오기
- 굳이 class까지는 필요 없을 듯
'''

from collections import deque

def check_gt(loc1, loc2):
    x1, y1 = loc1
    attack_time1, damage1 = time_map[x1][y1], damage_map[x1][y1]

    x2, y2 = loc2
    attack_time2, damage2 = time_map[x2][y2], damage_map[x2][y2]

    if loc1 == (-1, -1) or loc2 == (-1, -1):
        return True

    if damage1 != damage2:
        return damage1 > damage2
    elif attack_time1 != attack_time2:
        return attack_time1 < attack_time2
    elif (x1 + y1) != (x2 + y2):
        return (x1 + y1) < (x2 + y2)
    elif y1 != y2:
        return y1 < y2

    return False

def find_attacker():
    loc = (-1, -1)

    for x in range(N):
        for y in range(M):
            if not damage_map[x][y]:
                continue
            elif check_gt(loc, (x, y)):
                loc = (x, y)

    # 공격 시간, 공격력 갱신
    damage_map[loc[0]][loc[1]] += (N + M)
    time_map[loc[0]][loc[1]] = k + 1

    return loc


def find_target():
    loc = (-1, -1)

    for x in range(N):
        for y in range(M):
            if not damage_map[x][y]:
                continue
            elif (x, y) == attacker:
                continue
            elif check_gt((x, y), loc):
                loc = (x, y)

    return loc


def bfs(queue):
    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx = (x + dx[i]) % N
            ny = (y + dy[i]) % M

            if not damage_map[nx][ny]:
                continue
            if visited[nx][ny] == -1:
                visited[nx][ny] = visited[x][y] + 1
                queue.append((nx, ny))


    return


def raser():
    x, y = attacker
    tx, ty = target

    num = visited[x][y]
    damage = damage_map[x][y]
    while num:
        for i in range(4):
            nx = (x + dx[i]) % N
            ny = (y + dy[i]) % M

            if visited[nx][ny] == (visited[x][y] - 1):
                # 공격 기록
                attack_map[nx][ny] = 1

                # 공격력 깎기
                if (nx, ny) == (tx, ty):
                    damage_map[nx][ny] = max(0, damage_map[nx][ny] - damage)
                else:
                    damage_map[nx][ny] = max(0, damage_map[nx][ny] - (damage // 2))

                # 정보 갱신
                x, y = (nx, ny)
                num -= 1

                break

    return


def bomb():
    x, y = attacker
    tx, ty = target

    damage = damage_map[x][y]
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            nx = (tx + i) % N
            ny = (ty + j) % M

            if (nx, ny) == (x, y):
                continue
            elif (nx, ny) == (tx, ty):
                damage_map[nx][ny] = max(0, damage_map[nx][ny] - damage)
            else:
                damage_map[nx][ny] = max(0, damage_map[nx][ny] - (damage // 2))

            attack_map[nx][ny] = 1

    return


def attack():
    global visited, attack_map

    ax, ay = attacker
    tx, ty = target

    attack_map = [[0 for _ in range(M)] for _ in range(N)]
    attack_map[ax][ay] = 1

    visited = [[-1 for _ in range(M)] for _ in range(N)]
    queue = deque()

    visited[tx][ty] = 0
    queue.append((tx, ty))
    bfs(queue)

    # 레이저 공격 가능한 지 확인
    if visited[ax][ay] != -1:
        raser()
    else:
        bomb()

    return


def num_tower():
    num = 0
    for x in range(N):
        for y in range(M):
            if damage_map[x][y]:
                num += 1

    return num


def heal():
    for x in range(N):
        for y in range(M):
            if damage_map[x][y] and (not attack_map[x][y]):
                damage_map[x][y] += 1

    return


N, M, K = map(int, input().split())

damage_map = [list(map(int, input().split())) for _ in range(N)]
time_map = [[0 for _ in range(M)] for _ in range(N)]

# 우 하 좌 상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

for k in range(K):
    attacker = find_attacker()

    target = find_target()

    attack()
    # 만약 포탑이 하나만 남으면, 즉시 게임 종료
    if num_tower() == 1:
        break

    heal()

# 가장 높은 데미지
answer = -1
for x in range(N):
    for y in range(M):
        answer = max(answer, damage_map[x][y])

print(answer)