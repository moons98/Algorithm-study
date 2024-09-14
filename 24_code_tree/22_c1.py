
'''
start : 21:00
end : 23:30

회고 :
    - class를 통해서 멤버 변수에 한 번에 접근하는 방식이 때로는 도움이 된다
    - 점수를 얻는 시점에 대해서 고민 (움직여서 총을 주운 뒤가 아니라 대결 시점의 상태를 기준으로 계산됨)

nxn 격자

빨간색 숫자
    - 총 : 공격력
    - 사람 : 초기 능력치
노란색 숫자
     - 사람 : 사람 번호

### 1번부터 n번까지 순차적으로 진행 ###

1. 첫 번째 플레이어부터 본인이 향하는 방향으로 한 칸 이동
    - 격자를 벗어나는 경우에는 정 반대 방향으로 한 칸 이동
2. 이동한 방향에
    - 플레이어가 있다면 : 싸움
        - 초기 능력치 + 총의 공격력 >> 초기 능력치가 큰 사람이 승리
            - 패배한 플레이어는 가지고 있는 총을 해당 격자에 내려 놓고, 원래 가지고 있는 방향대로 한 칸 이동
                - 다른 플레이어가 있거나 격자 밖 -> 오른쪽으로 90도 회전 및 이동
                - 해당 칸에 총이 있다면 가장 공격력이 높은 총 획득
            - 승리한 플레이어는 (초기 능력치 - 총의 공격력의 합) 만큼의 포인트 획득
                - 가장 공격력이 높은 총 획득

    - 플레이어가 없으면 : 총이 있는지 확인
        - 총 발견, 이미 총이 있는 경우, 총들 중 공격력이 더 쎈 총 획득, 나머지 총은 해당 격자에 둠

플레이어들이 획득한 포인트 출력
'''

class Player:
    def __init__(self, x, y, d, s):
        self.x = x
        self.y = y
        self.d = d
        self.stat = s
        self.gun = 0

    def __gt__(self, other):
        if self.stat + self.gun > other.stat + other.gun:
            return self.stat + self.gun > other.stat + other.gun
        elif self.stat + self.gun == other.stat + other.gun:
            return self.stat > other.stat

    def move(self):
        nx, ny = self.x + dx[self.d], self.y + dy[self.d]

        # 격자 밖을 벗어나면
        if nx < 0 or nx >= n or ny < 0 or ny >= n:
            self.d = (self.d + 2) % 4

            self.x += dx[self.d]
            self.y += dy[self.d]
        else:
            self.x = nx
            self.y = ny

    def run(self):
        '''
        - 패배한 플레이어는 가지고 있는 총을 해당 격자에 내려 놓고, 원래 가지고 있는 방향대로 한 칸 이동
        - 다른 플레이어가 있거나 격자 밖 -> 오른쪽으로 90도 회전 및 이동
        - 해당 칸에 총이 있다면 가장 공격력이 높은 총 획득
        '''
        if self.gun:
            gun_map[self.x][self.y].append(self.gun)

        self.gun = 0

        for _ in range(4):
            nx = self.x + dx[self.d]
            ny = self.y + dy[self.d]

            if nx < 0 or nx >= n or ny < 0 or ny >= n or player_map[nx][ny] != -1:
                self.d = (self.d + 1) % 4
                continue

            self.x = nx
            self.y = ny

            break

    def change_gun(self):
        x, y = self.x, self.y
        if gun_map[x][y]:
            gun_map[x][y].sort()

            # 총의 공격력 비교
            if gun_map[x][y][-1] > self.gun:
                new_gun = gun_map[x][y].pop(-1)
                if self.gun:
                    gun_map[x][y].append(self.gun)

                self.gun = new_gun

    def print_player(self):
        print('Player status')
        print(f'player.x : {self.x}')
        print(f'player.y : {self.y}')
        print(f'player.d : {self.d}')
        print(f'player.s : {self.stat}')
        print(f'player.gun : {self.gun}')


# n은 격자의 크기, m은 플레이어의 수, k는 라운드의 수
n, m, k = map(int, input().split())

# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 숫자 0은 빈 칸, 0보다 큰 값은 총의 공격력
gun_map = [[[] for _ in range(n)] for _ in range(n)]
for x in range(n):
    for y, val in enumerate(list(map(int, input().split()))):
        if val:
            gun_map[x][y].append(val)


# (x, y)는 플레이어의 위치, d는 방향, s는 플레이어의 초기 능력치
player_map = [[-1 for _ in range(n)] for _ in range(n)]
player_lst = []

for i in range(m):
    x, y, d, s = map(int, input().split())

    new_player = Player(x-1, y-1, d, s)

    player_map[x-1][y-1] = i
    player_lst.append(new_player)


# k 라운드 진행
answer = [0 for _ in range(m)]
for _ in range(k):
    for i in range(m):
        cur_player = player_lst[i]

        # 움직이기 전 위치 지워줌
        player_map[cur_player.x][cur_player.y] = -1

        # 움직임
        player_lst[i].move()
        x, y = player_lst[i].x, player_lst[i].y


        # 다른 플레이어와 만났을 경우
        if player_map[x][y] != -1:
            other_num = player_map[x][y]
            other_player = player_lst[other_num]
            
            # 해당 플레이어가 승리
            if cur_player > other_player:
                # 포인트 획득
                answer[i] += (cur_player.stat + cur_player.gun) - (other_player.stat + other_player.gun)

                # 이전 위치 지워주기
                player_map[other_player.x][other_player.y] = -1
                other_player.run()
                player_map[other_player.x][other_player.y] = other_num

                # 총이 있으면 획득
                other_player.change_gun()

                # 총 획득
                cur_player.change_gun()

            # 다른 플레이어가 승리
            else:
                # 포인트 획득
                answer[other_num] += (other_player.stat + other_player.gun) - (cur_player.stat + cur_player.gun)

                # 이전 위치 지워주기
                cur_player.run()

                # 총이 있으면 획득
                cur_player.change_gun()

                # 총 획득
                other_player.change_gun()

        # 빈 칸일 경우, 총만 획득
        else:
            cur_player.change_gun()

        # 움직인 후 위치 갱신
        player_map[cur_player.x][cur_player.y] = i

for i in answer:
    print(i, end=' ')
