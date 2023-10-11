# -*- coding: utf-8 -*-
import sys


def check_row(cur_row):
    visited = [0 for _ in range(N)]

    for idx in range(1, N):
        if abs(cur_row[idx] - cur_row[idx - 1]) > 1:
            return False

        # 증가하는 경우, 이전 L개가 같은 숫자여야 함
        if cur_row[idx] - cur_row[idx - 1] == 1:
            tmp = cur_row[idx - 1]
            for i in range(1, L + 1):
                if idx - i < 0 or visited[idx - i] or cur_row[idx - i] != tmp:
                    return False
                else:
                    visited[idx - i] = 1
        # 감소하는 경우, 이후 L개가 같은 숫자여야 함
        elif cur_row[idx] - cur_row[idx - 1] == -1:
            tmp = cur_row[idx]
            for i in range(L):
                if idx + i >= N or visited[idx + i] or cur_row[idx + i] != tmp:
                    return False
                else:
                    visited[idx + i] = 1

    return True


N, L = map(int, sys.stdin.readline().split())
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

answer = 0
# 가로 방향 체크
for x in range(N):
    if check_row([map_lst[x][y] for y in range(N)]):
        answer += 1

# 세로 방향 체크
for y in range(N):
    if check_row([map_lst[x][y] for x in range(N)]):
        answer += 1

print(answer)


"""
질문 게시판에서 가로의 경사로와 세로의 경사로는 중복될 수 있음을 체크하고 시작

queue에 L개를 유지하면서 pop, append 하려다가 오히려 돌아감.
그냥 한 row씩 전달하면서 커지면 전의 L개, 작아지면 앞의 L개를 확인하면 되는 간단한 문제
"""
