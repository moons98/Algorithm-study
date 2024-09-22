
'''
산타의 선물 공장 2

start: 22:20
end:

회고 :
    - 300번 order가 성가심
        - 갯수가 (0,1), (1,0), (0,2), (2,0), (2,1), (2,3) 등등
    - 300번 order에서, 바꾼 노드의 nxt 노드의 prv 노드 값을 바꿔주지 않아서 생기는 문제 발견 못함


벨트의 정보와 선물의 정보를 조회할 수 있는 기능 추가

1. 공장 설립
    - n개의 벨트, m개의 물건 준비
    - m개의 선물의 위치가 주어짐

2. 물건 전부 옮기기
    - m_src번째 벨트의 선물을 m_dst번째 벨트로 옮김
    - m_src번째 벨트에 선물 없으면 동작 x
    - 옮긴 뒤, m_dst번째 벨트의 선물 갯수 출력

3. 앞 물건만 교체
    - m_src번째 선물 중 가장 앞의 선물을 m_dst번째 벨트와 교체
    - 둘 중 하나에 선물 없으면 옮기기만 함
    - 옮긴 뒤, m_dst번째 벨트의 선물 갯수 출력

4. 물건 나누기
    - m_src번째 벨트의 선물 갯수 n, 앞에서부터 floor(n/2)번째까지의 선물을 옮김
    - 선물이 1개인 경우, 옮기지 않음

5. 선물 정보 얻기
    - 선물 번호 p_num이 주어질 때, 앞 선물의 번호 a + 뒷 선물의 번호 b * 2 출력
    - 앞 선물이 없는 경우 a=-1, 뒷 선물이 없는 경우 b=-1

6. 벨트 정보 얻기
    - 벨트 번호 b_num, 맨 앞 선물 a, 맨 뒷 선물 b, 해당 벨트의 선물 갯수 c
    - (a + 2*b + 3*c) 출력
    - 선물 없는 경우, (a = b = -1)

- 기본적으로는 double linked-list 사용
- 갯수를 출력해야 하므로, global 변수로 갯수를 유지하자
- 선물의 id로부터 belt_num을 봐야 하는 경우는 없음
- belt 갯수가 10만개까지 가능, 벨트 정보는 다 dict 형태로
'''

class Present():
    def __init__(self, prv, nxt):
        self.prv = prv
        self.nxt = nxt


def print_status():
    tmp_map = [[] for _ in range(n)]

    # 각 node의 head를 따라 가며 append
    for idx, head in belt_head.items():
        while head:
            tmp_map[idx].append({head: [present[head].prv, present[head].nxt]})
            head = present[head].nxt

    for i in tmp_map:
        print(i)

    return


def order100(tmp):
    global n, m, present, belt_head, belt_tail, num_present

    # n개 벨트, m개 선물
    n, m, *B_num = tmp

    # 각 벨트의 head, tail
    belt_head = dict()
    belt_tail = dict()
    for i in range(n):
        belt_head[i] = None
        belt_tail[i] = None

    # 모든 선물을 쌓아둘 임시 변수
    tmp_present = [[] for _ in range(n)]
    for idx, val in enumerate(B_num):
        # belt는 0부터 시작, 선물 id는 1부터 시작
        tmp_present[val - 1].append(idx + 1)

    # 선물 class를 저장할 dict
    present = dict()
    for belt_num, belt_lst in enumerate(tmp_present):
        # head, tail 값 갱신
        if belt_lst:
            belt_head[belt_num] = belt_lst[0]
            belt_tail[belt_num] = belt_lst[-1]
        else:
            continue

        # 각 벨트 별로 순회
        prv_present = None
        for _p in belt_lst:
            cur_present = _p
            present[_p] = Present(prv_present, None)

            # 이전 node의 nxt 값 갱신
            if prv_present:
                present[prv_present].nxt = cur_present

            prv_present = cur_present

    # 전체 선물 갯수
    num_present = dict()
    for idx, val in enumerate(tmp_present):
        num_present[idx] = len(val)

    return


def order200(tmp):
    m_src, m_dst = tmp
    
    # idx 맞춰 주기
    src = m_src - 1
    dst = m_dst - 1
    
    # 만약 src에 선물이 있다면
    if num_present[src]:
        # 기존 값들 변수화
        dst_head, dst_tail = belt_head[dst], belt_tail[dst]
        src_head, src_tail = belt_head[src], belt_tail[src]

        # 새로운 head 연결, 기존 node 연결
        # node가 존재함, head만 바꿔주면 됨
        if dst_head:
            belt_head[dst] = src_head

            present[src_tail].nxt = dst_head
            present[dst_head].prv = src_tail

        # node가 없음, head와 tail을 모두 바꿔줘야 함
        else:
            belt_head[dst] = src_head
            belt_tail[dst] = src_tail

        # src 정보 삭제
        belt_head[src] = belt_tail[src] = None

        # 선물 갯수 바꿔주기
        num_present[dst] += num_present[src]
        num_present[src] = 0

    answer.append(num_present[dst])

    return


def order300(tmp):
    m_src, m_dst = tmp

    src = m_src - 1
    dst = m_dst - 1

    # 둘 다 없으면
    if (not belt_head[src]) and (not belt_head[dst]):
        pass

    # (dst -> src) only
    elif (not belt_head[src]):
        # 옮기고자 하는 타겟
        target = belt_head[dst]

        # 다음 선물이 있으면, dst의 다음 선물을 head로 바꿔줌
        target_nxt = present[target].nxt
        if target_nxt:
            belt_head[dst] = target_nxt
            present[target_nxt].prv = None
        # 선물이 하나였다면, head = tail = None
        else:
            belt_head[dst] = None
            belt_tail[dst] = None

        # dst -> src
        belt_head[src] = target
        belt_tail[src] = target
        present[target].nxt = None

        # 갯수 조정
        num_present[src] += 1
        num_present[dst] -= 1

    # (src -> dst) only
    elif (not belt_head[dst]):
        # 옮기고자 하는 타겟
        target = belt_head[src]

        # 다음 선물이 있으면, src의 다음 선물을 head로 바꿔줌
        target_nxt = present[target].nxt
        if target_nxt:
            belt_head[src] = target_nxt
            present[target_nxt].prv = None
        # 선물이 하나였다면, head = tail = None
        else:
            belt_head[src] = None
            belt_tail[src] = None

        # src -> dst
        belt_head[dst] = target
        belt_tail[dst] = target
        present[target].nxt = None

        # 갯수 조정
        num_present[dst] += 1
        num_present[src] -= 1
    
    # 둘 다 있을 경우
    else:
        # 기존 값들 변수화
        dst_head, dst_tail = belt_head[dst], belt_tail[dst]
        src_head, src_tail = belt_head[src], belt_tail[src]

        # head, tail 정보 바꿔주기
        belt_head[dst] = src_head
        belt_head[src] = dst_head

        # node 정보 바꿔주기
        tmp_present = Present(present[src_head].prv, present[src_head].nxt)
        present[src_head] = Present(present[dst_head].prv, present[dst_head].nxt)
        present[dst_head] = Present(tmp_present.prv, tmp_present.nxt)

        # 만약 갯수가 한 개라면 tail도 바꿔줘야 함
        if dst_head == dst_tail:
            belt_tail[dst] = src_head
        else:
            present[present[src_head].nxt].prv = src_head

        if src_head == src_tail:
            belt_tail[src] = dst_head
        else:
            present[present[dst_head].nxt].prv = dst_head

    answer.append(num_present[dst])

    return


def order400(tmp):
    m_src, m_dst = tmp

    src = m_src - 1
    dst = m_dst - 1

    num = num_present[src] // 2
    if num:
        # 기존 src, dst 벨트 정보
        dst_head = belt_head[dst]
        src_head = belt_head[src]

        cur_present = belt_head[src]
        for _ in range(num - 1):
            cur_present = present[cur_present].nxt

        # src의 새로운 head 갱신
        new_src_head = present[cur_present].nxt

        belt_head[src] = new_src_head
        present[new_src_head].prv = None

        # dst의 head 갱신
        belt_head[dst] = src_head

        # 기존에 선물이 없었으면, tail도 갱신
        if not dst_head:
            belt_tail[dst] = cur_present
            present[cur_present].nxt = None
        # src 끝과 dst 처음 연결해주기
        else:
            present[cur_present].nxt = dst_head
            present[dst_head].prv = cur_present

        # 갯수 조정
        num_present[src] -= num
        num_present[dst] += num

    answer.append(num_present[dst])

    return


def order500(p_num):
    a = present[p_num].prv if present[p_num].prv else -1
    b = present[p_num].nxt if present[p_num].nxt else -1

    answer.append(a + 2*b)

    return


def order600(b_num):
    num = b_num - 1

    a = belt_head[num] if belt_head[num] else -1
    b = belt_tail[num] if belt_tail[num] else -1
    c = num_present[num]

    answer.append(a + 2*b + 3*c)

    return


q = int(input())

answer = []
for _ in range(q):
    order, *tmp = map(int, input().split())

    if order == 100:
        order100(tmp)
    elif order == 200:
        order200(tmp)
    elif order == 300:
        order300(tmp)
    elif order == 400:
        order400(tmp)
    elif order == 500:
        order500(*tmp)
    elif order == 600:
        order600(*tmp)

for i in answer:
    print(i)


'''
14
100 4 6 1 2 2 2 1 4
200 2 4
300 4 2
300 2 4
300 1 4
400 4 2
400 1 2
400 1 3
500 6
500 5
500 1
600 1
600 3
600 2
'''