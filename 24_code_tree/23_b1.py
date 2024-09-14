def print_map():
    new_map = copy.deepcopy(map_lst)
    new_map[exit_loc[0]][exit_loc[1]] = -1

    for i in new_map:
        print(i)

'''
start: 22:52
end: 01:30

회고 :
    - square를 찾는 방법이 잘못됨
    - 단순히 people을 sort하고 돌리면 될 줄 알았는데, 아님
    - 결국 우선순위는 만들어진 박스의 좌상단이 기준이기 때문에 좌상단 위치를 구해 봐야 비교할 수 있음!!

M명의 참가자

- 미로는 NxN 격자 (r,c) 좌표
    - 좌상단은 (1,1)
- 각 칸은 3가지 중 하나의 상태를 가짐
    1) 빈 칸
        - 참가자 이동 가능
    2) 벽
        - 참가자 이동 불가능
        - 1이상 9이하의 내구도 가짐
        - 회전할 때, 내구도가 1씩 깎임
        - 내구도가 0이 되면, 빈 칸으로 변경
    3) 출구
        - 참가자가 해당 칸 도달 시 즉시 탈출

---

1. 1초마다 모든 참가자는 한 칸씩 움직임
    - 두 위치의 최단거리는 L2-norm
    - 모든 참가자는 동시에 움직임
    - 상하좌우로, 벽이 없는 곳으로 이동 가능
    - 움직일 수 있는 칸이 2개 이상이면, 상하 >> 좌우
    - 움직일 수 없으면, stay
    - 한 칸에 2명 이상의 참가자 존재 가능

2. 미로 회전
    - 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형 찾기
    - 2개 이상이라면, r 작을수록 >> c 작을수록
    - 정사각형은 시계 방향으로 90도 회전, 회전된 벽은 내구도 -1

K초 전에 참가자 모두가 탈출 -> 게임 종료
게임 종료 시, 모든 참가자들의 이동 거리 합과 출구 좌표 출력
'''

import copy


def move():
    global move_distance, people

    tx, ty = exit_loc

    new_people = copy.deepcopy(people)
    for idx, (x, y) in people.items():
        loc = []

        # 상하 움직임 비교
        if (tx - x) > 0:
            loc.append(1)
        elif (tx - x) < 0:
            loc.append(0)

        # 좌우 움직임 비교
        if (ty - y) > 0:
            loc.append(3)
        elif (ty - y) < 0:
            loc.append(2)

        if not loc:
            continue

        # 움직일 수 있으면
        loc.sort()

        for d in loc:
            nx, ny = x + dx[d], y + dy[d]

            # 벽이 가로막고 있으면
            if map_lst[nx][ny]:
                continue
            else:
                move_distance += 1

                # 만약 출구 도착하면
                if (nx, ny) == (tx, ty):
                    new_people.pop(idx)
                else:
                    new_people[idx] = (nx, ny)

                break

    people = new_people

    return


def find_square():
    tx, ty = exit_loc

    # 가장 가까운 거리와 사람 위치 찾기
    distance = N
    loc = []
    for _, (x, y) in people.items():
        # 가장 거리 큰 값
        tmp = max(abs(tx - x), abs(ty - y))

        # 우하단 좌표 찾기
        lower_right = (max(x, tx), max(y, ty))
        upper_left = (max(0, lower_right[0] - tmp), max(0, lower_right[1] - tmp))

        if tmp < distance:
            distance = tmp
            loc = [upper_left]
        elif tmp == distance:
            loc.append(upper_left)

    loc.sort(key=lambda x:(x[0], x[1]))

    return loc[0], distance


def rotate():
    global map_lst, exit_loc

    upper_left, distance = find_square()

    new_map = copy.deepcopy(map_lst)
    for x in range(distance + 1):
        for y in range(distance + 1):
            # 벽일 경우 내구도 -1
            new_map[y + upper_left[0]][distance - x + upper_left[1]] = max(0, map_lst[x + upper_left[0]][y + upper_left[1]] -1)

    # 사람이 위치할 경우 위치 변경
    for idx, (x, y) in people.items():
        if (upper_left[0] <= x <= upper_left[0] + distance) and (upper_left[1] <= y <= upper_left[1] + distance):
            diff_x, diff_y = x - upper_left[0], y - upper_left[1]
            people[idx] = (diff_y + upper_left[0], distance - diff_x + upper_left[1])

    # 출구 위치 변경
    tx, ty = exit_loc
    diff_x, diff_y = tx - upper_left[0], ty - upper_left[1]
    exit_loc = (diff_y + upper_left[0], distance - diff_x + upper_left[1])

    map_lst = new_map

    return


N, M, K = map(int, input().split())

map_lst = [list(map(int, input().split())) for _ in range(N)]

people = dict()
for i in range(M):
    x, y = map(int, input().split())
    people[i] = (x-1, y-1)

x, y = map(int, input().split())
exit_loc = (x-1, y-1)

# 상, 하, 좌, 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

move_distance = 0
for _ in range(K):
    move()
    if not people:
        break

    rotate()
    if not people:
        break

print(move_distance)
for i in exit_loc:
    print(i+1, end=' ')
