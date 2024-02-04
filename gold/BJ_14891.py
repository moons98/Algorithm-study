# -*- coding: utf-8 -*-
import sys
from collections import deque


def check_rotate(num, check_num):
    # 내가 더 큰 값 -> 내 9시와 상대 3시 확인
    # 3시 계산법 : (idx + 4) % 8
    if (
        num > check_num
        and gear[num][idx_lst[num]] != gear[check_num][(idx_lst[check_num] + 4) % 8]
    ):
        return True
    elif (
        num < check_num
        and gear[num][(idx_lst[num] + 4) % 8] != gear[check_num][idx_lst[check_num]]
    ):
        return True

    return False


def rotate_gear(rep_state):
    global idx_lst

    queue = deque()
    for i in rep_state:
        queue.append(i)
        visited = [0 for _ in range(4)]
        while queue:
            num, method = queue.popleft()
            visited[num] = 1

            # 주변 기어 확인
            for val in [-1, 1]:
                # 확인할 기어 번호
                check_num = num + val
                if 0 <= check_num <= 3 and not visited[check_num]:
                    if check_rotate(num, check_num):
                        queue.append([check_num, method * -1])

            # 회전으로 idx 변경
            idx_lst[num] = (idx_lst[num] + (method * -1)) % 8

    return


def cal_score():
    answer = 0
    for idx, num in enumerate(idx_lst):
        if gear[idx][(num + 2) % 8]:
            answer += 2**idx

    return answer


gear = []
idx_lst = [6 for _ in range(4)]
for _ in range(4):
    tmp = sys.stdin.readline().rstrip()
    gear.append(list(int(i) for i in tmp))

rep = int(sys.stdin.readline())
rep_state = []
for _ in range(rep):
    tmp = list(map(int, sys.stdin.readline().split()))
    rep_state.append([tmp[0] - 1, tmp[-1]])

### 동작 시작
rotate_gear(rep_state)
print(cal_score())

"""
9시 방향의 idx만 운용을 하고, 회전 시 이 값만 바꿔서 판단하기
9시부터 시계 방향으로 갈수록 1씩 증가 ("0" 1 '2' 3 "4" 5 6 7) -> 중앙값: (idx + 2) % 8
1: 시계, -1: 반시계

- 기어 회전
    - 해당 위치 좌우가 이미 회전한 기어인지 확인
    - 아닐 경우 나와 맞대는 극 확인하기
    - 극 반대일 경우 회전 (나와 반대 방향으로) -> queue에 추가

-> 중앙 idx를 주는데 9시 방향인 줄 알고 코드를 짜서 좀 복잡해짐... 지문 확인 잘 하기!!
"""
