'''
산타의 선물 공장

start: 08:50
end: 11:05

회고 :
    - 순회를 하고 싶지 않았는데, 어쩧 수 없이 belt_num 갱신을 위해 했어야 했음
        - 시간 초과가 안남 -> 500이 최대 10번까지만 주어질 수 있고, 선물 10만개라서 그런듯
    -  조건을 좀 덕지덕지 붙여서 명확하지 않은 부분 있음
         - 실제로 제출하고 한 번 틀렸는데, 실제 상황이었으면 못 찾았음
         - 조건 좀 명료하게 바꾸기


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


- 각 벨트의 head, tail 노드를 유지
- 각 노드는 head, tail 노드를 가지는 double linked-list
    - 실제 구현은 {id : [head, tail]}의 dict 구조로 가져감
'''

class Node:
    def __init__(self, left, right, num, weight):
        self.left = left
        self.right = right
        
        # 몇 번째 벨트에 위치했는지, 무게
        self.num = num
        self.weight = weight


def print_status():
    global belt_map

    belt_map = [[] for _ in range(m)]

    for i in range(m):
        head = belt_head[i]
        tail = belt_tail[i]

        if head == tail == None:
            continue

        belt_map[i].append({head: [box[head].left, box[head].right]})

        if head == tail:
            continue

        cur_id = head
        while True:
            cur_id = box[cur_id].right
            belt_map[i].append({cur_id: [box[cur_id].left, box[cur_id].right]})

            if cur_id == tail:
                break

    for i in belt_map:
        print(i)

    return


def order100(tmp):
    global n, m, belt_head, belt_tail, box, belt_status

    n, m, id_weight = tmp[0], tmp[1], tmp[2:]
    box_per_belt = n // m

    # belt의 head, tail
    belt_head = [None for _ in range(m)]
    belt_tail = [None for _ in range(m)]
    belt_status = [1 for _ in range(m)]

    # box_info
    box = dict()

    prev_id = None
    for i in range(n):
        belt_num = i // box_per_belt
        loc = i % box_per_belt

        if loc == 0:
            prev_id = None

        cur_id, _weight = id_weight[i], id_weight[n + i]

        # head와 tail 정보를 갱신
        if loc == 0:
            belt_head[belt_num] = cur_id

        elif loc == (box_per_belt -1):
            belt_tail[belt_num] = cur_id

        # 각 노드 정보 갱신
        box[cur_id] = Node(prev_id, None, belt_num, _weight)

        if prev_id:
            box[prev_id].right = cur_id

        prev_id = cur_id

    return


def order200(w_max):
    cur_answer = 0

    for idx, head_id in enumerate(belt_head):
        if head_id == None:
            continue

        cur_node = box[head_id]
        l_node, r_node, weight = cur_node.left, cur_node.right, cur_node.weight

        # belt의 head 바꿔주기, 다음 노드의 left 없애주기
        belt_head[idx] = r_node
        box[r_node].left = None

        # 무게가 넘으면 삭제
        if box[head_id].weight <= w_max:
            box.pop(head_id)
            cur_answer += weight
        # 무게가 넘지 않으면 맨 뒤로
        else:
            before_tail = belt_tail[idx]
            # 기존 tail의 right 정보, cur_node의 l/r 정보
            box[before_tail].right = head_id
            cur_node.left = before_tail
            cur_node.right = None

            # tail 정보 수정
            belt_tail[idx] = head_id

    answer.append(cur_answer)

    return


def order300(r_id):
    cur_answer = -1

    # 만약 존재하는 박스라면
    if r_id in box.keys():
        cur_node = box.pop(r_id)
        left_node, right_node, num = cur_node.left, cur_node.right, cur_node.num

        if left_node == right_node == None:
            belt_head[num] = None
            belt_tail[num] = None

        # 현재 노드가 head
        elif left_node == None:
            belt_head[num] = right_node
            box[right_node].left = None
        elif right_node == None:
            belt_tail[num] = left_node
            box[left_node].right = None

        # left_node의 right - right_node의 left 연결
        else:
            box[left_node].right = right_node
            box[right_node].left = left_node

        cur_answer = r_id

    answer.append(cur_answer)

    return


def order400(f_id):
    cur_answer = -1

    # 만약 상자가 있다면
    if f_id in box.keys():
        left_node, right_node, num = box[f_id].left, box[f_id].left, box[f_id].num

        # 기존 head, tail는 더이상 head가 아님
        before_head = belt_head[num]
        before_tail = belt_tail[num]

        # 기존에 f_id 왼쪽 값이 tail이 됨
        belt_tail[num] = left_node
        if left_node:
            box[left_node].right = None

        # f_id가 head가 됨
        belt_head[num] = f_id
        box[f_id].left = None

        # 기존 head의 앞에 기존 tail을 붙여줌
        if before_head:
            box[before_head].left = before_tail

        if before_tail:
            box[before_tail].right = before_head

        cur_answer = num + 1

    answer.append(cur_answer)

    return


def order500(b_num):
    cur_answer = -1

    # 기존에 벨트가 고장나지 않았다면
    if belt_status[b_num - 1]:
        belt_status[b_num - 1] = 0

        check_order = [i for i in range(b_num, m)] + [i for i in range(b_num-1)]
        for i in check_order:
            if belt_status[i]:
                new_num = i
                break

        # 고장난 벨트의 head가 옆 벨트의 tail 뒤에 붙음
        broken_head, broken_tail, broken_num = belt_head[b_num - 1], belt_tail[b_num - 1], b_num -1
        new_tail = belt_tail[new_num]

        # 고장난 벨트에 아무 것도 없을 경우
        if broken_head == broken_tail == None:
            pass

        # 새로운 벨트가 비어 있는 경우
        elif new_tail == None:
            belt_head[new_num] = belt_head[b_num - 1]
            belt_tail[new_num] = belt_tail[b_num - 1]

            # 바뀐 belt number 바꿔줘야 함
            cur_node = broken_head
            while True:
                box[cur_node].num = new_num

                cur_node = box[cur_node].right
                if cur_node == None:
                    break

        # 둘 다 최소 하나씩의 노드 가지면
        else:
            # 기존 tail과 고장난 head 연결
            box[new_tail].right = broken_head
            box[broken_head].left = new_tail

            # 바뀐 tail 처리
            belt_tail[new_num] = broken_tail

            # 바뀐 belt number 바꿔줘야 함
            cur_node = broken_head
            while True:
                box[cur_node].num = new_num

                cur_node = box[cur_node].right
                if cur_node == None:
                    break

        # 고장난 벨트 처리
        belt_head[b_num - 1] = None
        belt_tail[b_num - 1] = None

        cur_answer = b_num

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

'''
7
100 12 3 10 12 20 15 14 19 22 25 16 17 21 18 30 30 20 20 10 18 17 15 25 11 14 17
200 25
300 25
300 19
300 22
400 18
500 3
'''