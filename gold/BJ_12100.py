# -*- coding: utf-8 -*-
import sys
from collections import deque
from copy import deepcopy


def cal_map(maps, dx, dy):
    new_map = deepcopy(maps)
    # 좌우 움직임
    if dx == 0 and dy == -1:
        for i in range(N):
            val = -1
            nums = []
            for j in range(N):
                if maps[i][j] == 0:
                    continue
                elif val == -1:
                    val = maps[i][j]
                elif val == maps[i][j]:
                    nums.append(val * 2)
                    val = -1
                else:
                    nums.append(val)
                    val = maps[i][j]
            if val != -1:
                nums.append(val)

            nums += [0 for _ in range(N - len(nums))]
            new_map[i] = nums

    elif dx == 0 and dy == 1:
        for i in range(N):
            val = -1
            nums = []
            for j in range(N - 1, -1, -1):
                if maps[i][j] == 0:
                    continue
                elif val == -1:
                    val = maps[i][j]
                elif val == maps[i][j]:
                    nums.append(val * 2)
                    val = -1
                else:
                    nums.append(val)
                    val = maps[i][j]
            if val != -1:
                nums.append(val)

            nums = [0 for _ in range(N - len(nums))] + nums[::-1]
            new_map[i] = nums

    # 상하 움직임
    elif dx == -1 and dy == 0:
        # 열 번호 의미
        for i in range(N):
            val = -1
            nums = []
            for j in range(N):
                if maps[j][i] == 0:
                    continue
                elif val == -1:
                    val = maps[j][i]
                elif val == maps[j][i]:
                    nums.append(val * 2)
                    val = -1
                else:
                    nums.append(val)
                    val = maps[j][i]
            if val != -1:
                nums.append(val)

            nums += [0 for _ in range(N - len(nums))]
            for k in range(N):
                new_map[k][i] = nums[k]

    elif dx == 1 and dy == 0:
        # 열 번호 의미
        for i in range(N):
            val = -1
            nums = []
            for j in range(N - 1, -1, -1):
                if maps[j][i] == 0:
                    continue
                elif val == -1:
                    val = maps[j][i]
                elif val == maps[j][i]:
                    nums.append(val * 2)
                    val = -1
                else:
                    nums.append(val)
                    val = maps[j][i]
            if val != -1:
                nums.append(val)

            nums = [0 for _ in range(N - len(nums))] + nums[::-1]
            for k in range(N - 1, -1, -1):
                new_map[k][i] = nums[k]

    return new_map


def bfs(init_map, val):
    queue = deque()
    queue.append([init_map, val])

    final_map = []
    while queue:
        tmp_map, tmp_val = queue.popleft()
        for i in range(4):
            new_map = cal_map(tmp_map, dx[i], dy[i])
            if tmp_val + 1 != 5:
                queue.append([new_map, tmp_val + 1])
            else:
                final_map.append(new_map)

    answer = 0
    for i in final_map:
        for j in i:
            answer = max(answer, max(j))

    return answer


N = int(sys.stdin.readline())
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]
answer = bfs(map_lst, 0)
print(answer)

# n = cal_map(map_lst, dx[2], dy[2])
# for i in n:
#     print(i)

"""
완전탐색으로 접근
받은 maps를 copy할 때, maps[:]의 얕은 복사로 접근해서 아래 예제가 다 합쳐져버리는 오류 발생

8
2 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0
16 0 0 0 0 0 0 0
32 0 0 0 0 0 0 0
64 0 0 0 0 0 0 0
128 0 0 0 0 0 0 0
"""
