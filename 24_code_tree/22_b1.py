'''
start: 11:30
end: 13:30

회고 :
    - 시작 및 공 던지는 방향 설정에 대해서 디버깅을 하지 않았음 -> 충분히 제출하고 틀릴 수 있었음
    - queue에서는 뒤집는 연산이 reverse(), list에 쓸 경우 NoneType이 return
    - 원하는 idx에 넣는 함수 : insert

nxn 격자
3명 이상이 한 팀

1. 머리 사람을 따라서 한 칸 이동
2. 정해진 선을 따라 공이 던져짐
    - 최초에 만나는 사람의 번호 ** 2 만큼의 점수를 얻음 (머리 사람부터 몇 번째)
3. 공을 획득한 팀의 머리 사람과 꼬리 사람이 바뀜


공 맞기 전
[[1, 2, 3, 4], [5, 6, 7, 8, 9]], tail_idx: 3

공 맞은 후
[[4, 3, 2, 1], [9, 8, 7, 6, 5]], tail_idx: 3 유지

'''

def dfs(x, y):
    visited[x][y] = group_num
    tmp_loc.append((x, y))

    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]

        # 움직일 수 없는 위치
        if nx < 0 or nx >= n or ny < 0 or ny >= n:
            continue
        elif visited[nx][ny]:
            continue
        elif map_lst[nx][ny] == 0:
            continue
        # 머리 사람을 만나는 경우에는 멈춰야 함
        elif map_lst[nx][ny] == 1:
            return

        if map_lst[nx][ny] == 3:
            tail[group_num] = len(tmp_loc)

        dfs(nx, ny)

    return


def move():
    global map_lst, group_loc

    # map_lst 재구성
    new_map = [[0 for _ in range(n)] for _ in range(n)]

    for idx, loc in group_loc.items():
        _tmp = loc.pop()
        loc = [_tmp] + loc
        group_loc[idx] = loc

        for i in range(tail[idx] + 1):
            x, y = loc[i]
            new_map[x][y] = i + 1

    map_lst = new_map

    return


def throw_ball(loc, d):
    global answer

    nx, ny = loc[0] - d[0], loc[1] - d[1]
    for i in range(n):
        nx += d[0]
        ny += d[1]

        if map_lst[nx][ny] == 0:
            continue

        # 사람 만나면 점수 증가
        answer += map_lst[nx][ny] ** 2

        # 위치 순서 바꾸기
        target_group = visited[nx][ny]

        new_loc = group_loc[target_group][:tail[target_group] + 1][::-1] + group_loc[target_group][(tail[target_group] + 1):][::-1]
        group_loc[target_group] = new_loc

        return

    return


n, m, k = map(int, input().split())

group_loc = dict()

map_lst = [list(map(int, input().split())) for _ in range(n)]

# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 각 그룹의 꼬리사람 idx
tail = dict()

# 그룹 별 동선 식별하기
visited = [[0 for _ in range(n)] for _ in range(n)]

group_num = 1
for x in range(n):
    for y in range(n):
        if not visited[x][y] and map_lst[x][y] == 1:
            # 시작 위치
            tmp_loc = [(x, y)]
            visited[x][y] = group_num
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]

                # 움직일 수 없는 위치
                if nx < 0 or nx >= n or ny < 0 or ny >= n:
                    continue

                # 두 번째 사람의 방향이면 진행
                elif map_lst[nx][ny] == 2:
                    dfs(nx, ny)

                    group_loc[group_num] = tmp_loc
                    group_num += 1
                    break

answer = 0
start_loc = [(0,0), (n-1, 0), (n-1, n-1), (0, n-1)]
move_set = [(1,0), (0,1), (-1,0), (0,-1)]
for i in range(k):
    move()

    _a = i // (n)
    _b = i % (n)

    _c = _a % 4

    sx = start_loc[_c][0] + move_set[_c][0] * _b
    sy = start_loc[_c][1] + move_set[_c][1] * _b

    if _c == 0:
        throw_ball((sx, sy), (0,1))
    elif _c == 1:
        throw_ball((sx, sy), (-1,0))
    elif _c == 2:
        throw_ball((sx, sy), (0,-1))
    elif _c == 3:
        throw_ball((sx, sy), (1,0))


print(answer)
