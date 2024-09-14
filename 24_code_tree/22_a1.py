'''
start : 23:07
end : 03:23

회고 :
    - chaser를 tuple로 사용했는데 tuple에 담긴 내용 비교 안하고 그냥 가져다가 씀, (x, y)와 (x, y, d)를 비교하고 있었음;;
    - 달팽이 회전 및 reverse 회전에서 방향을 어떻게 유지해야 할 지 고민함

nxn 격자
m명의 도망자 -> 각각 좌'우' / 상'하'만 움직이는 유형, 바라보는 방향 존재
h개의 나무

1. 도망자가 동시에 움직임
    - 바라보고 있는 칸에 술래가 있으면 움직이지 않음
    - 술래가 없다면 움직임, 나무도 ㄱㅊ
    - 바라보고 있는 방향이 잘못됨 -> 방향 틀고 전진 시도
2. 술래가 움직임
    - 달팽이 모양으로 움직임
    - 끝에 도달하면 다시 중앙을 향해 반대로 움직임
    - 이동 후에 이동방향이 틀어지는 지점이라면 방향을 바로 틀어줌
    
... k번 반복

술래와의 거리가 3 이하인 도망자만 움직임 - L1 norm
술래의 시야는 3칸
나무가 있는 칸이라면, 가려져서 보이지 않음
t번째 턴 x 도망자의 수 만큼 점수 얻음
'''


# 도망자 움직임
def move_people():
    global map_lst, people
    for id, (x, y, d) in people.items():
        if abs(chaser[0] - x) + abs(chaser[1] - y) <= 3:
            nx, ny = x + dx[d], y + dy[d]
            
            # 진행 가능한 경우
            if not (nx < 0 or nx >= n or ny < 0 or ny >= n):
                # 술래를 만나는 경우
                if (nx, ny) == (chaser[0], chaser[1]):
                    continue
                else:
                    # 이동
                    people[id] = (nx, ny, d)
                    map_lst[x][y].remove(id)
                    map_lst[nx][ny].append(id)

            # 움직일 수 없는 경우
            else:
                d = (d+2) % 4
                nx, ny = x + dx[d], y + dy[d]
                if (nx, ny) != (chaser[0], chaser[1]):
                    # 이동
                    people[id] = (nx, ny, d)
                    map_lst[x][y].remove(id)
                    map_lst[nx][ny].append(id)

    return


def move_chaser(idx):
    global chaser, dir_loc
    x, y, d = chaser

    nx, ny = x + dx[d], y + dy[d]

    # 방향 바꾸기
    if dir_loc[0] == idx:
        dir_loc.pop(0)
        dir_loc.append(idx)

        if idx <= flag_cnt1:
            d = (d + 1) % 4
        else:
            d = (d - 1) % 4

        if idx == flag_cnt1:
            d = (d + 1) % 4
        elif idx == flag_cnt2:
            d = (d - 1) % 4

    chaser = (nx, ny, d)

    return


# 술래가 잡을 수 있는 도망자 cnt
def cal_score():
    global map_lst, people
    x, y, d = chaser

    score = 0
    # 현재 위치 체크
    if map_lst[x][y] and (-1 not in map_lst[x][y]):
        for id in map_lst[x][y]:
            people.pop(id)

        score += len(map_lst[x][y])
        map_lst[x][y] = []

    for i in range(2):
        x += dx[d]
        y += dy[d]

        # 격자 벗어나는 경우
        if x < 0 or x >= n or y < 0 or y >= n:
            return score
        # 나무 or 비어 있는 경우가 아니면
        elif map_lst[x][y] and (-1 not in map_lst[x][y]):
            for id in map_lst[x][y]:
                people.pop(id)

            score += len(map_lst[x][y])
            map_lst[x][y] = []

    return score


n, m, h, k = map(int, input().split())

# 우, 하, 좌, 상 ->  (+2) %4 하고 거꾸로 인덱스 돌아야 방향 전환됨
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

map_lst = [[[] for _ in range(n)] for _ in range(n)]

# 도망자 정보, id 달아서 dict로 저장
people = dict()
for i in range(m):
    # d==1 -> 좌'우' / d==2 -> 상'하'
    x, y, d = map(int, input().split())

    loc = 0 if d == 1 else 1
    people[i] = (x-1, y-1, loc)
    map_lst[x-1][y-1].append(i)

# 나무 위치
tree = []
for _ in range(h):
    x, y = map(int, input().split())
    tree.append((x-1, y-1))
    map_lst[x-1][y-1].append(-1)


# 술래 위치
chaser = (n//2, n//2, 3)

# 달팽이 회전
# 1,1, 2,2, 3,3, 4,4 순서로 커짐
# n//2 + 1 번째 위로 향하는 방향은 값 안 커지고, 같은 값만큼 위로 무빙 후 끝
dir_loc = []

_cnt = 1
for i in range((n//2)*4):
    # 횟수
    dir_loc.append(_cnt)
    if i % 2 == 1:
        _cnt += 1

# 마지막 위쪽 방향
dir_loc.append(_cnt - 1)
flag_cnt1 = sum(dir_loc) -1
dir_loc += dir_loc[::-1]

dir_loc[0] -= 1
for i in range(1, len(dir_loc)):
    dir_loc[i] += dir_loc[i-1]
flag_cnt2 = max(dir_loc)

answer = 0
cycle = dir_loc[-1] + 1

for i in range(k):
    move_people()
    move_chaser(i % cycle)
    answer += cal_score() * (i+1)

print(answer)
