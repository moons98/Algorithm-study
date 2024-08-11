# import sys
# sys.stdin = open("input.txt", "r")

'''
가로 M, 세로 N
빨간 구슬을 구멍을 통해서 빼내는 것, 파란 구슬은 들어가면 안 됨
기울이기 동작
빨, 파 구슬이 동시에 빠져도 실패
더 이상 구슬이 움직이지 않을 때까지 굴림
최소 몇 번 만에 구슬을 빼낼 수 있는지 구하기
10번 이하로 빼낼 수 없으면 -1 출력

BFS로 움직인 횟수, 구슬 위치 유지하게

fail: cnt 세는 부분에서 11번까지 동작하게 만들어짐
'''


from collections import deque

# 우 하 좌 상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]


def bfs():
    visited = []
    while queue:
        cnt, [rx, ry], [bx, by] = queue.popleft()

        # check finish
        if cnt + 1 > 10:
            return -1

        # each direction
        for i in range(4):
            # red biz
            n_rx, n_ry = rx, ry
            while True:
                n_rx += dx[i]
                n_ry += dy[i]

                if map_lst[n_rx][n_ry] == '#':
                    n_rx -= dx[i]
                    n_ry -= dy[i]
                    break
                elif map_lst[n_rx][n_ry] == 'O':
                    break

            # blue biz
            n_bx, n_by = bx, by
            while True:
                n_bx += dx[i]
                n_by += dy[i]

                if map_lst[n_bx][n_by] == '#':
                    n_bx -= dx[i]
                    n_by -= dy[i]
                    break
                elif map_lst[n_bx][n_by] == 'O':
                    break

            # 파란 구슬이 빠진 경우
            if map_lst[n_bx][n_by] == 'O':
                continue

            # 같은 위치인 경우
            if [n_rx, n_ry] == [n_bx, n_by]:
                # 구슬이 같은 위치에 있는 경우 -> 더 많이 움직인 애들 한 칸 뒤로
                if abs(n_rx - rx) + abs(n_ry - ry) > abs(n_bx - bx) + abs(n_by - by):
                    n_rx -= dx[i]
                    n_ry -= dy[i]
                else:
                    n_bx -= dx[i]
                    n_by -= dy[i]

            # 종료 조건 확인
            if map_lst[n_rx][n_ry] == 'O':
                return cnt + 1

            # 방문한 적 없는 기울임
            if [n_rx, n_ry, n_bx, n_by] not in visited:
                visited.append([n_rx, n_ry, n_bx, n_by])
                queue.append([cnt+1, [n_rx, n_ry], [n_bx, n_by]])

    return -1


N, M = list(map(int, input().split()))

map_lst = []
for i in range(N):
    tmp = input().rstrip()
    for idx, j in enumerate(tmp):
        if j == 'R':
            red_biz = [i, idx]
        elif j == 'B':
            blue_biz = [i, idx]

    map_lst.append(tmp)


queue = deque()
queue.append([0, red_biz, blue_biz])
print(bfs())