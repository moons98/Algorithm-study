'''
나무 타이쿤

start: 22:40
end: 23:10

회고:
    - 영양제가 있는 칸을 기록해서 시간 복잡도를 n^2 -> k로 줄일 수 있음을 알아 둘 것

- nxn 격자
- 특수 영양제
    - 1x1 땅에 있는 리브로수의 높이를 1 증가시킴
    - 씨앗만 있는 경우 높이 1의 리브로수를 만들어냄
    - 초기에 좌하단 4개 칸에 주어짐

- 특수 영양제의 움직임
    - 이동 규칙은 이동 방향과 이동 칸 수로 주어짐
    - 반대편으로 나오는 움직임 가질 수 있음

1. 특수 영양제를 이동 규칙에 따라 이동
2. 해당 땅에 특수 영양제 투입, 해당 특수 영양제는 사라짐
3. 영양제 투입한 리브로수의 대각선으로 인접한 방향에 높이가 1 이상인 리브로수가 있는 만큼 높이 성장
    - 격자를 벗어나는 방향인 경우에는 세지 않음
4. 영양제 투입 리브로수를 제외, 높이가 2인 리브로수는 높이 2를 베고, 영양제를 자리에 올려둠

남아 있는 리브로수 높이들의 총 합
'''

def move():
    global sup_map

    new_sup = [[0 for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if not sup_map[x][y]:
                continue

            # 영양제가 있는 칸이라면
            nx = (x + (dx[d] * p)) % n
            ny = (y + (dy[d] * p)) % n

            new_sup[nx][ny] = 1

            # 식물 성장
            map_lst[nx][ny] += 1

    sup_map = new_sup

    return


def grow():
    for x in range(n):
        for y in range(n):
            if not sup_map[x][y]:
                continue

            cnt = 0
            for i in range(4):
                nx, ny = x + diag_dx[i], y + diag_dy[i]

                if nx < 0 or nx >= n or ny < 0 or ny >= n:
                    continue

                # 식물 수 카운트
                if map_lst[nx][ny]:
                    cnt += 1

            map_lst[x][y] += cnt

    return


def make_sup():
    global sup_map

    new_sup = [[0 for _ in range(n)] for _ in range(n)]

    for x in range(n):
        for y in range(n):
            if sup_map[x][y]:
                continue

            # 높이가 2 이상이면 영양제로 만듦
            if map_lst[x][y] >= 2:
                map_lst[x][y] -= 2
                new_sup[x][y] = 1

    sup_map = new_sup

    return


n, m = map(int, input().split())

map_lst = [list(map(int, input().split())) for _ in range(n)]

# 영양제 존재하는 map
sup_map = [[0 for _ in range(n)] for _ in range(n)]
init_sup = [(n-1, 0), (n-2, 0), (n-1, 1), (n-2, 1)]
for (x, y) in init_sup:
    sup_map[x][y] = 1

order = []
for _ in range(m):
    _d, p = list(map(int, input().split()))
    order.append((_d-1, p))

# → ↗ ↑ ↖ ← ↙ ↓ ↘
dx = [0, -1, -1, -1, 0, 1, 1, 1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]

# ↗ ↖ ↙ ↘
diag_dx = [-1, -1, 1, 1]
diag_dy = [1, -1, -1, 1]

for (d, p) in order:
    move()

    grow()

    make_sup()

answer = 0
print(sum(sum(i) for i in map_lst))