# -*- coding: utf-8 -*-
import sys


def pile_bowl_90(bowl_lst):
    num, rep = N, 2
    # 돌리는 높이보다 남은 길이가 더 길어야 함
    while len(bowl_lst[0]) <= num - (rep // 2):
        num -= rep // 2
        new_bowl = bowl_lst[rep // 2 :]

        # 어항 회전해서 쌓기
        for i in bowl_lst[: rep // 2][::-1]:
            for idx, j in enumerate(i):
                new_bowl[idx].append(j)

        rep += 1
        bowl_lst = new_bowl

    return new_bowl


"""
(1,1) (2,1) (2,2) (3,2) (3,3) (4,3)
"""


def pile_bowl_180(bowl_lst):
    new_bowl = [i[:] for i in bowl_lst]
    for i in range(2, 5, 2):
        target = new_bowl[: N // i]
        new_bowl = new_bowl[N // i :]

        for idx, i in enumerate(target[::-1]):
            for j in i[::-1]:
                new_bowl[idx].append(j)

    return new_bowl


def move_fish(bowl_lst):
    new_bowl = [i[:] for i in bowl_lst]
    for x, val1 in enumerate(bowl_lst):
        for y, val2 in enumerate(val1):
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if 0 <= nx < len(bowl_lst) and 0 <= ny < len(bowl_lst[nx]):
                    tmp = (val2 - bowl_lst[nx][ny]) // 5
                    # 한쪽 기준으로만 움직여줘야 함, 안그러면 2번 같은작업 발생
                    if tmp > 0:
                        new_bowl[x][y] -= tmp
                        new_bowl[nx][ny] += tmp

    return new_bowl


def expand_bowl(bowl_lst):
    new_bowl = []
    for i in bowl_lst:
        for j in i:
            new_bowl.append([j])

    return new_bowl


N, K = map(int, sys.stdin.readline().split())
fishbowl = list(map(int, sys.stdin.readline().split()))

dx = [0, -1, 0, 1]
dy = [1, 0, -1, 0]

answer = 0
while True:
    max_fish, min_fish = max(fishbowl), min(fishbowl)
    if max_fish - min_fish <= K:
        break

    # 1. 물고기 추가
    for idx, val in enumerate(fishbowl):
        if val == min_fish:
            fishbowl[idx] += 1

    # 2. 어항 쌓기
    bowl_lst = [[i] for i in fishbowl]
    bowl_lst = pile_bowl_90(bowl_lst)
    bowl_lst = move_fish(bowl_lst)
    bowl_lst = expand_bowl(bowl_lst)
    bowl_lst = pile_bowl_180(bowl_lst)
    bowl_lst = move_fish(bowl_lst)
    bowl_lst = expand_bowl(bowl_lst)

    answer += 1
    fishbowl = [i[0] for i in bowl_lst]

print(answer)

"""
1. 물고기 추가 (가장 수가 적은 어항, 중복 허용)
2. 어항 쌓기 (가장 왼쪽에 있는 어항을 옆에 올림)
    -> deque 사용해서 popleft로 처음 N개 자르기 
3. 어항 회전 (2개 이상 쌓인 어항을 공중부양 후 시계방향 90도 회전, 쌓기 -> 안될때까지)
4. 물고기 조절 (인접 어항에 대해서 물고기 수 차이가 5마리당 1마리씩 옮김, 동시에 진행)
5. 어항 펼치기 (좌하단부터 펼침)
6. 어항 쌓기 (절반씩 시계방향 180도 회전, 2번 반복)
7. 물고기 조절 (인접 어항에 대해서 물고기 수 차이가 5마리당 1마리씩 옮김, 동시에 진행)
8. 어항 펼치기 (방법 5와 같음)

물고기가 가장 많은 어항 - 적은 어항 <= K가 되기 위한 반복 횟수

지문에서 7번 물고기 조절을 빼먹어서 디버깅에 시간 소요함;;
"""
