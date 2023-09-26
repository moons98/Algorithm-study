# -*- coding: utf-8 -*-
import sys


def dfs(x, y, visited, dsum, cnt):
    global answer
    visited[x][y] = 1

    if cnt == 4:
        answer = max(answer, dsum)
        visited[x][y] = 0
        return

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if 0 <= nx < N and 0 <= ny < M and not visited[nx][ny]:
            dfs(nx, ny, visited, dsum + map_lst[nx][ny], cnt + 1)

    visited[x][y] = 0

    return


# ㅗ 모양의 최댓값 계산
def except_block(x, y):
    global answer

    for i in range(4):
        tmp = map_lst[x][y]
        for j in range(3):
            loc = (i + j) % 4
            nx = x + move[loc][0]
            ny = y + move[loc][1]
            if 0 <= nx < N and 0 <= ny < M:
                tmp += map_lst[nx][ny]
            else:
                tmp = 0
                break
        answer = max(answer, tmp)
        # print("exec", answer)

    return


N, M = map(int, sys.stdin.readline().split())
map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
visited = [[0 for _ in range(M)] for _ in range(N)]

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

move = [(1, 0), (0, 1), (-1, 0), (0, -1)]

answer = 0
for i in range(N):
    for j in range(M):
        dfs(i, j, visited, map_lst[i][j], 1)
        except_block(i, j)

print(answer)


"""
반복을 줄이려고 방향을 오른쪽, 아래로 제한했는데, ㅗ 모양의 처리를 못함
dfs에서 visited 전달할 때, 이 경우에는 좌표가 지나감에 따라 visited가 계속 초기화가 되어야 하므로 0으로 꺼주는 작업 필요
"""
