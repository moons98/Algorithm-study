# -*- coding: utf-8 -*-
import sys


def check_straight():
    for y in range(n):
        start_idx = y
        for x in range(h):
            if map_lst[x][start_idx] == 1:
                start_idx += 1
            elif start_idx > 0 and map_lst[x][start_idx - 1] == 1:
                start_idx -= 1
        if start_idx != y:
            return False

    return True


def dfs(cnt, x, y):
    global answer

    if cnt >= answer:
        return
    if check_straight():
        answer = min(answer, cnt)
        return
    if cnt == 3:
        return

    for i in range(x, h):
        # 열 중간에 넘어온거면 y부터, 아니면 0번 열부터 체크
        y_idx = y if i == x else 0
        for j in range(y_idx, n - 1):
            if map_lst[i][j] == 0 and map_lst[i][j + 1] == 0:
                map_lst[i][j] = 1
                dfs(cnt + 1, i, j + 2)
                map_lst[i][j] = 0

    return


"""
답안 참고함ㅠ
- 자신의 왼쪽은 체크할 필요가 없음 -> j+2로 dfs 돌리기에 왼쪽은 자동으로 걸러줌
- check_straight 돌린 이후, cnt==3일때는 무조건 넘김 -> 루프 돌아서 dfs는 계속 호출되는데, 결국 cnt==4짜리라 결국 다 return됨
    -> 미리 넘기면 안되는게, 3에서 True면 answer 갱신해야 함
    -> 그렇다고 check_straight 하고 cnt 체크하기에는 불필요한 연산량이 너무 들어감


H x N 격자
i번 세로선의 결과가 i가 나와야 함!

추가해야 하는 가로선의 갯수 출력
3 이상, 혹은 불가능하면 -1 출력
"""

n, m, h = map(int, sys.stdin.readline().split())

map_lst = [[0 for _ in range(n)] for _ in range(h)]

# 가로선 긋기 (a, b)
for _ in range(m):
    a, b = map(int, sys.stdin.readline().split())
    map_lst[a - 1][b - 1] = 1

answer = 4
dfs(0, 0, 0)
print(-1 if answer == 4 else answer)
