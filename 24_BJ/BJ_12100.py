

def print_map():
    for i in map_lst:
        print(i)

    return

'''
brute-force로 접근
map_lst도 복사해서 전달 필요
'''

from collections import deque


def move_right(cnt, tmp_map):
    new_map = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        flag = 0
        idx = N-1
        for j in range(N-1, -1, -1):
            if tmp_map[i][j] == 0:
                continue

            # 기준점이 없을 경우
            if not flag:
                flag = tmp_map[i][j]

            # 기준점과 같을 경우
            elif tmp_map[i][j] == flag:
                new_map[i][idx] = flag*2
                idx -= 1
                flag = 0
            else:
                new_map[i][idx] = flag
                idx -= 1
                flag = tmp_map[i][j]

        # 마지막 숫자
        if flag:
            new_map[i][idx] = flag

    if cnt + 1 == 5:
        return max(max(new_map))
    else:
        queue.append([cnt+1, new_map])

    return 0


def move_left(cnt, tmp_map):
    new_map = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        flag = 0
        idx = 0
        for j in range(N):
            if tmp_map[i][j] == 0:
                continue

            # 기준점이 없을 경우
            if not flag:
                flag = tmp_map[i][j]

            # 기준점과 같을 경우
            elif tmp_map[i][j] == flag:
                new_map[i][idx] = flag*2
                idx += 1
                flag = 0
            else:
                new_map[i][idx] = flag
                idx += 1
                flag = tmp_map[i][j]

        # 마지막 숫자
        if flag:
            new_map[i][idx] = flag

    if cnt + 1 == 5:
        return max(max(new_map))
    else:
        queue.append([cnt+1, new_map])

    return 0


def move_down(cnt, tmp_map):
    new_map = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        flag = 0
        idx = N-1
        for j in range(N-1, -1, -1):
            if tmp_map[j][i] == 0:
                continue

            # 기준점이 없을 경우
            if not flag:
                flag = tmp_map[j][i]

            # 기준점과 같을 경우
            elif tmp_map[j][i] == flag:
                new_map[idx][i] = flag*2
                idx -= 1
                flag = 0
            else:
                new_map[idx][i] = flag
                idx -= 1
                flag = tmp_map[j][i]

        # 마지막 숫자
        if flag:
            new_map[idx][i] = flag

    if cnt + 1 == 5:
        return max(max(new_map))
    else:
        queue.append([cnt+1, new_map])

    return 0


def move_up(cnt, tmp_map):
    new_map = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        flag = 0
        idx = 0
        for j in range(N):
            if tmp_map[j][i] == 0:
                continue

            # 기준점이 없을 경우
            if not flag:
                flag = tmp_map[j][i]

            # 기준점과 같을 경우
            elif tmp_map[j][i] == flag:
                new_map[idx][i] = flag*2
                idx += 1
                flag = 0
            else:
                new_map[idx][i] = flag
                idx += 1
                flag = tmp_map[j][i]

        # 마지막 숫자
        if flag:
            new_map[idx][i] = flag

    if cnt + 1 == 5:
        return max(max(new_map))
    else:
        queue.append([cnt+1, new_map])

    return 0


N = int(input())
map_lst = [list(map(int, input().split())) for _ in range(N)]

global queue
queue = deque()
queue.append([0, map_lst])

answer = 0
while queue:
    cnt, tmp_map = queue.popleft()

    # # 우
    # answer = max(answer, move_right(cnt, tmp_map))
    # # 좌
    # answer = max(answer, move_left(cnt, tmp_map))
    # 하
    answer = max(answer, move_down(cnt, tmp_map))
    # # 상
    # answer = max(answer, move_up(cnt, tmp_map))

print(answer)

'''
3
2 4 8
2 4 8
2 4 8

3
2 0 4
0 2 4
8 4 4
'''