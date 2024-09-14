'''
start: 23:14
end : 24:40

회고 :
    - 우선 순위 계산하는 조건을 하나 빼먹음
    - priority queue를 사용하면 훨씬 빠르게 풀 수 있었음 -> 수행 시간이 5배 넘게 차이남
        - heaqp.heappush, heapq.heappop 함수 사용해서 구현 가능 !!!

1. 경주 시작 준비
    - P마리의 토끼, NxM 격자, 고유 번호, 꼭 이동해야 하는 거리 존재
    - 처음 토끼들은 전부 (1행, 1열)에 존재
2. 경주 진행
    - 가장 우선 순위가 높은 토끼를 뽑아 멀리 보내주는 것을 K번 반봅
    - 현재까지의 총 점프 횟수가 적은 >> 행+열이 작은 >> 행이 작은 >> 열이 작은 >> 고유 번호가 작은
    - 상하좌우로 d만큼 이동했을 때의 위치를 구함
        - 다음 칸이 격자를 벗어나게 된다면 반대로 방향을 바꿔 한 칸 이동
        - 4개의 위치 중, 행+열이 큰 >> 행이 큰 >> 열이 큰 순으로 우선순위를 둠
        - 해당 위치가 (r, c)일 때, 나머지 토끼들은 r+c만큼 점수를 얻음

    - K턴이 진행된 후, 행+열이 큰 >> 행이 큰 >> 열이 큰 >> 고유번호가 큰 순서로 우선순위를 둠
    - 우선순위가 가장 높은 토끼에게 +S점 
    - K번의 턴 동안 한 번이라도 뽑힌 적이 있던 토끼 중 골라야 함

3. 이동거리 변경
    - 고유번호가 pid인 토끼의 이동 거리를 L배
4. 최고의 토끼 선정
    - 가장 높은 점수를 출력

'''

class Rabbit():
    def __init__(self, pid, distance):
        self.x = 0
        self.y = 0
        self.pid = pid
        self.distance = distance
        self.jump_cnt = 0
        self.score = 0

    def __lt__(self, other):
        if self.jump_cnt != other.jump_cnt:
            return self.jump_cnt < other.jump_cnt
        elif (self.x + self.y) != (other.x + other.y):
            return (self.x + self.y) < (other.x + other.y)
        elif self.x != other.x:
            return self.x < other.x
        elif self.y != other.y:
            return self.y < other.y
        elif self.pid != other.pid:
            return self.pid < other.pid

    def __gt__(self, other):
        if (self.x + self.y) != (other.x + other.y):
            return (self.x + self.y) > (other.x + other.y)
        elif self.x != other.x:
            return self.x > other.x
        elif self.y != other.y:
            return self.y > other.y
        elif self.pid != other.pid:
            return self.pid > other.pid


def init(tmp):
    global N, M

    [N, M, P], _tmp = tmp[:3], tmp[3:]

    for i in range(P):
        pid, distance = _tmp[2*i : 2*(i+1)]
        new_rabbit = Rabbit(pid, distance)
        rabbits[pid] = new_rabbit

    return


def move_up(target):
    x, y, distance = target.x, target.y, target.distance

    distance %= (N - 1) * 2

    if distance <= x:
        x -= distance
    elif distance <= x + (N - 1):
        distance -= x
        x = distance
    else:
        distance -= x + (N - 1)
        x = N - 1 - distance

    return (x, y)


def move_down(target):
    x, y, distance = target.x, target.y, target.distance

    distance %= (N - 1) * 2

    if distance <= (N - 1 - x):
        x += distance
    elif distance <= (N - 1) * 2 - x:
        distance -= (N - 1 - x)
        x = N - 1 - distance
    else:
        distance -= (N - 1) * 2 - x
        x = distance

    return (x, y)


def move_right(target):
    x, y, distance = target.x, target.y, target.distance

    distance %= (M - 1) * 2

    if distance <= (M - 1 - y):
        y += distance
    elif distance <= (M - 1) * 2 - y:
        distance -= (M - 1 - y)
        y = M - 1 - distance
    else:
        distance -= (M - 1) * 2 - y
        y = distance

    return (x, y)


def move_left(target):
    x, y, distance = target.x, target.y, target.distance

    distance %= (M - 1) * 2

    if distance <= y:
        y -= distance
    elif distance <= y + (M - 1):
        distance -= y
        y = distance
    else:
        distance -= y + (M - 1)
        y = M - 1 - distance

    return (x, y)


def race(tmp):
    global accumulate_score

    K, S = tmp

    jumped_rabbit_pid = []
    for k in range(K):
        target = Rabbit(-1, -1)
        # 우선 순위가 높은 토끼 (총 점프 횟수가 적은 >> 행+열이 작은 >> 행이 작은 >> 열이 작은 >> 고유 번호가 작은)
        for pid, _rabbit in rabbits.items():
            if target.pid == -1 or _rabbit < target:
                target = _rabbit

        target.jump_cnt += 1
        if target.pid not in jumped_rabbit_pid:
            jumped_rabbit_pid.append(target.pid)

        # (상,하,좌,우) 순서로 도착 위치 찾기
        available_loc = []
        available_loc.append(move_up(target))
        available_loc.append(move_down(target))
        available_loc.append(move_right(target))
        available_loc.append(move_left(target))

        available_loc.sort(reverse=True, key=lambda x:(x[0]+x[1], x[0], x[1]))
        target.x, target.y = available_loc[0]

        # 점수 더할 때, r+1, c+1로 계산해야 됨 유의
        accumulate_score += (target.x + target.y + 2)
        target.score -= (target.x + target.y + 2)

    target = Rabbit(-1, -1)
    # 우선 순위가 높은 토끼 (행+열이 큰 >> 행이 큰 >> 열이 큰 >> 고유번호가 큰)
    for pid, _rabbit in rabbits.items():
        if _rabbit.pid not in jumped_rabbit_pid:
            continue
        elif target.pid == -1 or _rabbit > target:
            target = _rabbit

    target.score += S


    return


def change_distance(tmp):
    pid, L = tmp
    rabbits[pid].distance *= L

    return


def choose_best():
    _score = []
    for pid, _rabbits in rabbits.items():
        _score.append(_rabbits.score)

    print(accumulate_score + max(_score))

    return


Q = int(input())

rabbits = dict()

accumulate_score = 0
for _ in range(Q):
    order, *tmp = map(int, input().split())
    if order == 100:
        init(tmp)
    elif order == 200:
        race(tmp)
    elif order == 300:
        change_distance(tmp)
    elif order == 400:
        choose_best()
