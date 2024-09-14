
'''
산타의 선물 공장

start: 20:10
end: 21:30

회고 :
    - queue의 내장 함수들 기억할 필요 있음 -> 예를 들어 rotate, remove ,,,
    - queue는 slicing 함수가 없음, 삭제/삽입에만 특화, slicing은 list가 더 빠름
    - linked list로 풀지 않으면 slicing, indexing에서 시간 초과 발생


산타는 공장에서 순서대로 q개의 명령에 따라 일을 진행
일의 종류는 5가지로 나뉨

1. 공장 설립
    - 공장에 m개의 벨트 설치, 각 벨트 위에 n/m개의 물건을 놓아 n개의 물건 준비
    - 각 물건에는 고유 번호(id), 무게(w)가 존재
    - 번호는 달라도, 무게는 동일할 수 있음

2. 물건 하차 
    - 산타가 원하는 최대 무게 w_max가 주어짐
    - 1~m번까지의 벨트를 보며, 맨 앞의 선물 중 w_max 이하면 하차, 아니라면 벨트 맨 뒤로 보냄
    - 하차된 상자 무게의 총 합 출력

3. 물건 제거
    - 제거하기를 원하는 물건의 고유 번호 r_id
    - 있다면 벨트에서 상자 제거

4. 물건 확인
    - 확인하기를 원하는 물건의 고유 번호 f_id가 주어짐
    - 놓인 벨트가 있다면, 벨트 번호 출력, 없다면 -1 출력
    - 상자가 있는 경우, 해당 상자 위에 있는 모든 상자를 전부 앞으로 가져옴
    - 123'4'5 -> '4'5123

5. 벨트 고장
    - 고장 발생 벨트 b_num
    - 해당 벨트는 다시는 사용 불가
    - 바로 오른쪽 벨트부터 고장이 나지 않은 최초의 벨트 위로 상자들을 옮겨줌
    - 오른쪽에 없을 경우 1번부터 차례로 확인
    - 모든 벨트가 망가지는 경우는 없음


- dict 구조 사용해서 각 id의 상자가 어느 벨트 위에 있는지 관리
- 각 벨트는 queue 자료구조 사용
'''

from collections import deque

def order100(tmp):
    global n, m, id_to_belt, belt, id_to_weight, belt_state

    n, m, id_weight = tmp[0], tmp[1], tmp[2:]

    id_to_belt  = dict()
    belt = [deque() for _ in range(m)]
    id_to_weight = dict()
    belt_state = [1 for _ in range(m)]

    # n//m개씩 벨트에 올라감
    for i in range(n):
        _id, _weight = id_weight[i], id_weight[i + n]

        # box_id와 belt_num 매칭
        box_num = i // (n//m)
        id_to_belt[_id] = box_num

        # queue에 id 쌓기, dict 구조로 (id:weight) 가지기
        belt[box_num].append(_id)
        id_to_weight[_id] = _weight

    return


def order200(w_max):
    total_weight = 0
    for idx, queue in enumerate(belt):
        # 빈 벨트라면 skip
        if not queue:
            continue

        cur_box = queue.popleft()

        # 무게가 w_max 이하면 하차, dict에서도 삭제
        if id_to_weight[cur_box] <= w_max:
            total_weight += id_to_weight[cur_box]
            id_to_belt.pop(cur_box)
        # 아니면 벨트 맨 뒤로
        else:
            queue.append(cur_box)

    answer.append(total_weight)

    return


def order300(r_id):
    cur_answer = -1

    # r_id가 있다면 제거
    if r_id in id_to_belt.keys():
        belt_num = id_to_belt.pop(r_id)
        belt[belt_num].remove(r_id)
        cur_answer = r_id

    answer.append(cur_answer)

    return


def order400(f_id):
    cur_answer = -1

    if f_id in id_to_belt.keys():
        belt_num = id_to_belt[f_id]
        cur_answer = belt_num + 1

        # 해당 박스 포함, 위에 있는 상자를 전부 앞으로 옮김
        while True:
            _id = belt[belt_num].pop()
            belt[belt_num].appendleft(_id)

            if _id == f_id:
                break

    answer.append(cur_answer)

    return


def order500(b_num):
    # 이미 망가진 경우
    if not belt_state[b_num - 1]:
        cur_answer = -1
    else:
        belt_state[b_num - 1] = 0
        cur_answer = b_num

        check_belt = [i for i in range(b_num-1, m)] + [i for i in range(b_num - 1)]
        for i in check_belt:
            if belt_state[i]:
                belt[i] = belt[i] + belt[b_num - 1]

                # 망가진 벨트에 해당하는 id_to_belt 없애줌, id_to_belt 값 바꿔줌
                while belt[b_num - 1]:
                    cur_box = belt[b_num - 1].popleft()
                    id_to_belt[cur_box] = i

                break

    answer.append(cur_answer)

    return


q = int(input())

answer = []
for _ in range(q):
    order, *tmp = map(int, input().split())

    if order == 100:
        order100(tmp)
    elif order == 200:
        order200(*tmp)
    elif order == 300:
        order300(*tmp)
    elif order == 400:
        order400(*tmp)
    elif order == 500:
        order500(*tmp)

for i in answer:
    print(i)
