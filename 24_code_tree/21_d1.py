'''
팩맨

start: 17:50
end: 19:30

회고 :
    - 몬스터가 있는 위치만 시체를 만들어야 함
    - 첫 세 칸 움직임에 먹지 못하는 경우에도 움직여야 하는데, best_num이 0이라 움직이지를 못했음
    - 문제 꼼꼼하게 읽고 테케 여러가지 만들어서 접근해보자

- 4x4 격자
- m개의 몬스터와 1개의 팩맨
- 각각의 몬스터는 상하좌우, 대각선 방향 중 하나를 가짐


1. 몬스터 복제 시도
    - 몬스터는 현재의 위치에서 자신과 같은 방향을 가진 몬스터를 복제 (부화되지 않은 상태, 움직일 수 없음)
    - 현재 시점을 기준으로 몬스터와 동일한 방향을 지님

2. 몬스터 이동
    - 현재 자신이 가진 방향대로 한 칸 이동, 몬스터 시체 or 팩맨이 있거나 격자 벗어나면 가능할 때까지 반시계 방향으로 회전
    - 그럼에도 갈 수 없다면 해당 몬스터는 움직이지 않음
    
3. 팩맨 이동
    - 팩맨은 3칸을 이동, 각 이동마다 상화좌우의 선택지를 가짐
    - 몬스터를 가장 많이 먹을 수 있는 방향으로 움직임
    - '상좌하우' 우선순위
    - 먹어치운 자리에는 몬스터 시체를 남김, 알이나 움직이기 전에 같이 있었던 몬스터는 먹지 않음

4. 몬스터 시체 소멸
    - 몬스터 시체는 2턴동안만 유지됨
    
5. 몬스터 복제 완성
    - 알 형태였던 몬스터가 부화

'''
import copy

def copy_monster():
    global egg_map

    egg_map = copy.deepcopy(map_lst)

    return


def move_monster():
    global map_lst

    new_map = [[[] for _ in range(4)] for _ in range(4)]
    for x in range(4):
        for y in range(4):
            # 몬스터 순회
            for _d in map_lst[x][y]:
                for _ in range(8):
                    flag = True
                    nx, ny = x + dx[_d], y + dy[_d]

                    # 움직일 수 없으면
                    if nx < 0 or nx >= 4 or ny < 0 or ny >= 4:
                        flag = False
                    # 몬스터 시체
                    elif dead_map[nx][ny]:
                        flag = False
                    # 팩맨이 있으면
                    elif (nx, ny) == pack_man:
                        flag = False

                    if flag:
                        break
                    else:
                        _d = (_d + 1) % 8

                # 움직일 수 없는 상태면 그냥 넣어줌
                if not flag:
                    new_map[x][y].append(_d)
                # 나머지 상태면 움직이고 넣어줌
                else:
                    new_map[x + dx[_d]][y + dy[_d]].append(_d)

    # 새로운 맵 갱신
    map_lst = new_map

    return


def dfs(num_move, dir_lst, cur_num, cur_loc):
    global best_num, best_loc

    if num_move == 3:
        # 더 많이 먹을 수 있는 경우
        if cur_num > best_num:
            best_num = cur_num
            best_loc = dir_lst

        return

    _x, _y = cur_loc
    for _i in range(4):
        nx, ny = _x + pack_dx[_i], _y + pack_dy[_i]

        if nx < 0 or nx >= 4 or ny < 0 or ny >= 4:
            continue

        # 현재까지 잡아먹은 물고기 수 체크
        if not visited[nx][ny]:
            new_num = cur_num + len(map_lst[nx][ny])
        else:
            new_num = cur_num

        # 방문 표시
        visited[nx][ny] += 1

        dfs(num_move + 1, dir_lst + [_i], new_num, (nx, ny))

        # 방문 표시 해제
        visited[nx][ny] -= 1

    return


def move_pack_man():
    global best_num, best_loc, pack_man, visited

    # 최고로 많이 먹을 수 있는 몬스터 수와 방향
    best_num, best_loc = -1, []
    visited = [[0 for _ in range(4)] for _ in range(4)]

    dfs(0, [], 0, pack_man)
    
    # 위치 정보 가지고 팩맨 움직이기
    x, y = pack_man
    for d in best_loc:
        x += pack_dx[d]
        y += pack_dy[d]
        
        # 시체 카운트 갱신
        if map_lst[x][y]:
            dead_map[x][y] = 3

        # 맵에서 몬스터 삭제
        map_lst[x][y] = []

    # 팩맨 위치 갱신
    pack_man = (x, y)

    return


def delete_dead():
    for x in range(4):
        for y in range(4):
            dead_map[x][y] = max(dead_map[x][y]-1, 0)

    return


def complete_copy():
    for x in range(4):
        for y in range(4):
            if egg_map[x][y]:
                map_lst[x][y] += egg_map[x][y]

    return


# 몬스터 마리 수, 턴의 수
m, t = map(int, input().split())

_x, _y = map(int, input().split())
pack_man = (_x - 1, _y - 1)

map_lst = [[[] for _ in range(4)] for _ in range(4)]
dead_map = [[0 for _ in range(4)] for _ in range(4)]

for _ in range(m):
    _r, _c, _d = map(int, input().split())
    map_lst[_r-1][_c-1].append(_d-1)

# ↑, ↖, ←, ↙, ↓, ↘, →, ↗
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

# 상 좌 하 우
pack_dx = [-1, 0, 1, 0]
pack_dy = [0, -1, 0, 1]

for _t in range(t):
    copy_monster()

    move_monster()

    move_pack_man()

    delete_dead()

    complete_copy()

answer = 0
for x in range(4):
    for y in range(4):
        answer += len(map_lst[x][y])

print(answer)