def print_status():
    tmp_map = [[-1 for _ in range(M)] for _ in range(N)]
    for (x,y), tmp_tower in tower_dict.items():
        tmp_map[x][y] = tmp_tower.damage

    for i in tmp_map:
        print(i)

    return

'''
포탑 부수기

start: 22:55
end: 00:25

회고 :
    - 문제 조건 놓침 (자기 자신은 공격 받지 않음)
    - 가장 약한 포탑을 구하는 조건 놓침 (lt 써서 그냥 작은 것 기준으로 정렬해버림)

    - dict 구조에서 키를 통해 값 조회하거나 삭제하는 것은 O(1) 복잡도 (해쉬 테이블로 구현)
    - list에서 indexing 역시 O(1) 복잡도
    - attacker = tmp_tower : 얕은 복사
    - 그러나 내부의 값을 바꾸는 것이 아니라, for tmp_tower in tower_lst: 형식으로 접근하는 것은 새로운 메모리 주소를 할당 (변경 아님)
        - 따라서 tmp_tower가 가리키는 대상이 변한다고 attacker도 따라서 변하지는 않음


- NxM 격자, 모든 위치에는 포탑 존재
- 각 포탑은 공격력 존재, 0이하가 되면 파괴, 최초에 부서진 포탑이 있을 수 있음
- 부서지지 않은 포탑이 1개가 된다면, 그 즉시 중지

1. 부서지지 않은 포탑 중 가장 약한 포탑이 공격자로 선정
    - 공격자로 선정되면 공격력이 N+M만큼 증가
    - 가장 약한 포탑의 기준 : 공격력이 가장 낮은 >> 가장 최근에 공격한 >> 행+열이 큰 >> 열이 큰

2. 공격자의 공격
    - 자신을 제외한 가장 강한 포탑을 공격
    - 가장 강한 포탑은 가장 약한 포탑 선정 기준의 반대: 공격력이 가장 높은 >> 공격한 지 오래된 >> 행+열이 작은 >> 열이 작은
    - 공격은 레이저 먼저 시도 >> 포탄 공격 시도

2-1) 레이저 공격
    - 상하좌우 4개 방향으로 움직일 수 있음
    - 부서진 포탑이 있는 위치는 지나지 못함
    - 반대편으로 진행 가능
    - 공격자의 위치에서 공격 대상까지 최단 경로로 공격
    - 이러한 경로가 없으면 포탄 공격 진행, '우>하>좌>상' 우선순위로 먼저 움직인 경로가 선택
    - 공격 대상은 공격자 공격력 만큼 피해, 경로에 있는 포탑은 절반 만큼 피해

2-2) 포탄 공격
    - 공격 대상은 공격력 만큼 피해, 주위 8개의 방향의 포탑도 절반 만큼 피해
    - 공격자는 해당 공격에 영향 받지 않음
    - 반대편 격자까지 피해 미침

3. 포탑 부서짐
    - 공격력 0 이하인 포탑 파괴

4. 포탑 정비
    - 부서지지 않은 포탑 중, 공격과 무관한 포탑은 공격력이 1씩 올라감

K번의 턴이 종료된 이후, 가장 강한 포탑의 공격력 출력
'''

from collections import deque

class Tower:
    def __init__(self, x, y, damage, attack_time):
        self.x = x
        self.y = y
        self.damage = damage
        self.attack_time = attack_time

    def __lt__(self, other):
        # 약한 포탑 선정
        if self.damage != other.damage:
            return self.damage < other.damage
        elif self.attack_time != other.attack_time:
            return self.attack_time > other.attack_time
        elif (self.x + self.y) != (other.x + other.y):
            return (self.x + self.y) > (other.x + other.y)
        elif self.y != other.y:
            return self.y > other.y


def select_tower():
    # 가장 약한 포탑 : 공격력이 가장 낮은 >> 가장 최근에 공격한 >> 행+열이 큰 >> 열이 큰
    # 가장 강한 포탑 : 공격력이 가장 높은 >> 공격한 지 오래된 >> 행+열이 작은 >> 열이 작은
    attacker, target = None, None
    for _, tmp_tower in tower_dict.items():
        # 공격자 판단
        if (not attacker) or tmp_tower < attacker:
            attacker = tmp_tower

        # 타겟 판단
        if (not target) or target < tmp_tower:
            target = tmp_tower

    # 공격력 증가
    attacker.damage += (N + M)

    return attacker, target


def bfs():
    global visited

    queue = deque()
    visited = [[0 for _ in range(M)] for _ in range(N)]

    # 타겟부터 진행
    queue.append((tx, ty))
    visited[tx][ty] = 1

    while queue:
        x, y = queue.popleft()
        for i in range(4):
            # 반대쪽으로 나옴
            nx = (x + dx[i]) % N
            ny = (y + dy[i]) % M

            # 방문했거나 파괴된 포탑
            if visited[nx][ny]:
                continue
            elif (nx, ny) not in tower_dict:
                continue
            elif tower_dict[(nx, ny)].damage == 0:
                continue

            visited[nx][ny] = visited[x][y] + 1
            queue.append((nx, ny))

    return


def raser():
    target_num = visited[sx][sy] - 1
    cur_x, cur_y = sx, sy

    while target_num:
        for i in range(4):
            nx = (cur_x + dx[i]) % N
            ny = (cur_y + dy[i]) % M

            if visited[nx][ny] == target_num:
                # 공격력 감소
                if target_num != 1:
                    tower_dict[(nx,ny)].damage -= (tower_dict[(sx,sy)].damage // 2)
                else:
                    tower_dict[(nx,ny)].damage -= tower_dict[(sx,sy)].damage

                # 파괴된 타워 삭제
                if tower_dict[(nx,ny)].damage <= 0:
                    tower_dict.pop((nx, ny))

                # 공격 관련자 표시
                attack_map[nx][ny] = 1

                cur_x, cur_y = nx, ny
                target_num -= 1
                break

    return


def bomb():
    # 타겟 데미지
    tower_dict[(tx, ty)].damage -= tower_dict[(sx, sy)].damage

    # 파괴된 타워 삭제
    if tower_dict[(tx, ty)].damage <= 0:
        tower_dict.pop((tx, ty))

    # 나머지 타워 데미지
    for i in range(8):
        nx = (tx + dx[i]) % N
        ny = (ty + dy[i]) % M

        if (nx, ny) not in tower_dict:
            continue
        # 자기 자신 건너뛰기
        elif (nx, ny) == (sx, sy):
            continue

        # 파괴되지 않은 포탑이라면
        tower_dict[(nx, ny)].damage -=  (tower_dict[(sx, sy)].damage // 2)

        # 공격 관련자 표시
        attack_map[nx][ny] = 1

        # 파괴된 타워 삭제
        if tower_dict[(nx, ny)].damage <= 0:
            tower_dict.pop((nx, ny))

    return


def attack():
    # 공격 방법 선택
    bfs()

    if visited[sx][sy]:
        raser()
    else:
        bomb()

    return


def heal():
    for x in range(N):
        for y in range(M):
            if (not attack_map[x][y]) and ((x, y) in tower_dict):
                tower_dict[(x, y)].damage += 1

    return


N, M, K = map(int, input().split())

# NxM 격자
visited = [[0 for _ in range(M)] for _ in range(N)]
tower_dict = dict()

# 공격 관련 타워 저장 map
attack_map = [[0 for _ in range(M)] for _ in range(N)]

# 우 하 좌 상 // 좌상, 좌하, 우상, 우하
dx = [0, 1, 0, -1, -1, 1, -1, 1]
dy = [1, 0, -1, 0, -1, -1, 1, 1]


for i in range(N):
    tmp_lst = list(map(int, input().split()))
    for j, val in enumerate(tmp_lst):
        if val:
            tower_dict[(i, j)] = Tower(i, j , val, 0)

for k in range(1, K+1):
    attack_map = [[0 for _ in range(M)] for _ in range(N)]

    # 공격자, 타겟 선정
    attacker, target = select_tower()

    sx, sy = attacker.x, attacker.y
    tx, ty = target.x, target.y

    # 공격 정보 갱신
    attack_map[sx][sy] = 1
    attack_map[tx][ty] = 1
    attacker.attack_time = k

    # 공격 진행
    attack()

    # 남은 포탑이 하나라면 종료
    if len(tower_dict) == 1:
        break

    # 포탑 회복
    heal()

# 정답 출력
answer = 0
for _, tmp_tower in tower_dict.items():
    if tmp_tower.damage > answer:
        answer = tmp_tower.damage

print(answer)
