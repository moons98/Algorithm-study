'''
미로 타워 디펜스

start: 21:15
end: 22:35

회고 :
    - 달팽이 배열에서 마지막 원소는 n-1이 되어야 함
    - queue에서 꺼내 오는 원소가 0이면 그냥 넘겨야 함


- nxn 격자, 1,2,3번 몬스터들이 존재

1. 플레이어는 상하좌우 중, 주어진 공격 칸 수만큼 몬스터를 공격 및 없앨 수 있음
2. 비어있는 공간만큼 몬스터는 앞으로 이동하여 공간을 채움
3. 몬스터의 종류가 4번 이상 반복하여 나오면 해당 몬스터 또한 삭제
    - 삭제된 이후에는 몬스터를 당겨주고, 4번 이상 나오는 몬스터가 있을 경우 계속 삭제
4. 삭제가 끝난 뒤에는 몬스터를 차례로 나열하여 같은 숫자끼리 짝을 짓고 (개수, 크기)로 바꾸어서 다시 집어 넣음

- 새로 생긴 배열이 원래 격자의 범위를 넘는다면, 나머지는 무시
- 1, 3번 과정에서 삭제되는 몬스터의 번호는 점수에 합쳐짐
- 플레이어가 얻게 되는 점수 출력


- map 만들어서, 공격 범위만큼 몬스터 제거
- 이후 queue로 만들어서, 하나씩 확인 후 넣기 (4개 이상의 것들 삭제 가능)
- 다시 map으로 만들기
'''

from collections import deque

def attack(d, p):
    global answer

    x, y = start_loc

    for _ in range(p):
        x += dx[d]
        y += dy[d]

        cur_num = map_lst[x][y]
        answer.append(cur_num)

        map_lst[x][y] = 0

    return


def make_queue():
    global queue

    queue = deque()
    cur_dir = start_dir
    x, y = start_loc
    for i in dir_set:
        for j in range(i):
            x += dx[cur_dir]
            y += dy[cur_dir]

            num = map_lst[x][y]
            if num:
                queue.append(num)

        cur_dir = (cur_dir + 1) % 4

    queue.append(0)

    return


def remove():
    flag = False
    new_queue = deque()

    cnt = 1
    prev_num = -1
    cur_answer = 0
    while queue:
        cur_num = queue.popleft()
        if cur_num == prev_num:
            cnt += 1
        else:
            if cnt >= 4:
                flag = True

                # 점수 갱신
                cur_answer += (cnt * prev_num)

            # 4개 이하일 때, 숫자 추가
            elif prev_num != -1:
                new_queue.extend([prev_num for _ in range(cnt)])

            cnt = 1

        prev_num = cur_num

    new_queue.append(0)
    answer.append(cur_answer)

    return flag, new_queue


def check_duplicate():
    global queue

    num_queue = deque()

    # 중복 삭제
    flag = True
    while flag:
        flag, queue = remove()

    # (갯수, 크기) 순으로 정렬
    cnt = 1
    prev_num = -1
    while queue:
        cur_num = queue.popleft()
        if cur_num == prev_num:
            cnt += 1
        elif prev_num != -1:
            num_queue.extend([cnt, prev_num])
            cnt = 1

        prev_num = cur_num

    queue = num_queue

    return


def make_map():
    global map_lst

    new_map = [[0 for _ in range(n)] for _ in range(n)]
    cur_dir = start_dir
    x, y = start_loc
    for i in dir_set:
        for j in range(i):
            x += dx[cur_dir]
            y += dy[cur_dir]

            if queue:
                cur_num = queue.popleft()
                if cur_num:
                    new_map[x][y] = cur_num
            else:
                map_lst = new_map
                return

        cur_dir = (cur_dir + 1) % 4

    map_lst = new_map

    return


n, m = map(int, input().split())

map_lst = [list(map(int, input().split())) for _ in range(n)]

# map을 만들기 위한 dir_set
dir_set = []
for i in range(1, n):
    for _ in range(2):
        dir_set.append(i)

dir_set += [n-1]

# 우,하,좌,상 -> 좌,하,우,상
idx_to_dir = {0:2, 1:1, 2:0, 3:3}

order = []
for _ in range(m):
    _d, p = map(int, input().split())
    order.append([idx_to_dir[_d], p])

# 좌,하,우,상
dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]

start_dir = 0
start_loc = (n//2, n//2)

answer = []
for (d, p) in order:
    attack(d, p)

    make_queue()

    check_duplicate()

    make_map()

print(sum(answer))