'''
코드트리 메신저

start: 10:00
end:

회고:
    -


사내 메신저의 구조는 이진 트리
최상단 노드는 회사의 메인 채팅방, 자식 노드들은 부서별 채팅방

(1) 사내 메신저 준비
    - 0번부터 N번까지 N+1 개의 채팅방 존재
    - 매인 채팅방의 번호는 0번
    - 각 채팅방은 권한 authority를 가짐
    - 그 채팅방의 상위 authority만큼의 채팅방들에게 알림이 가는 방식

(2) 알림망 설정
    - 처음 모든 채팅방의 알림망 설정은 on
    - c번 채팅방의 알림망 설정을 반대로 바꿔줌
    - off가 되면, 자기 자신을 포함하여 아래에서 올라온 알림을 올려보내지 않음

(3) 권한 세기 변경
    - c번 채팅방의 권한 세기를 power로 변경

(4) 부모 채팅방 교환
    - 서로 부모를 바꿈

(5) 알림을 받을 수 있는 채팅방 조회
    - c번 채팅방까지 알림이 도달할 수 있는 서로 다른 채팅방의 수 출력


'''

def order100(tmp):
    global m_status, messenger, parent, authority

    # 메신저 on/off 상태
    m_status = [1 for _ in range(N+1)]

    # 메신저가 받을 수 있는 메시지 수
    messenger = [[0 for _ in range(21)] for _ in range(N+1)]

    parent, authority = dict(), dict()
    parent[0] = -1
    authority[0] = 0
    for i in range(1, N+1):
        cur_parent, cur_author = tmp[i-1], tmp[N+i-1]

        parent[i] = cur_parent
        authority[i] = cur_author

    for i in range(1, N+1):
        cur_node = i
        cur_parent = parent[i]
        cur_author = authority[i]

        # parent 따라가며, authority만큼 권한 부여
        while (cur_author != 0) and (cur_parent != -1) and (m_status[cur_node]):
            messenger[cur_parent][cur_author - 1] += 1

            cur_node = cur_parent
            cur_parent = parent[cur_parent]
            cur_author -= 1

    return


def on_2_off(c):
    # 해당 채팅방 위로 영향도 없앰
    cur_node = c
    cur_parent = parent[c]
    cur_author = authority[c]

    # 자신의 영향 없앰
    while (cur_author != 0) and (cur_parent != -1) and (m_status[cur_node]):
        messenger[cur_parent][cur_author - 1] -= 1

        cur_node = cur_parent
        cur_parent = parent[cur_parent]
        cur_author -= 1

    # 자신 밑으로부터의 영향 없앰
    for idx, val in enumerate(messenger[c]):
        if not val:
            continue

        cur_node = c
        cur_parent = parent[c]
        cur_author = idx

        # 자신의 영향 없앰
        while (cur_author != 0) and (cur_parent != -1) and (m_status[cur_node]):
            messenger[cur_parent][cur_author - 1] -= val

            cur_node = cur_parent
            cur_parent = parent[cur_parent]
            cur_author -= 1

    m_status[c] = 0

    return


def off_2_on(c):
    # 해당 채팅방 위로 영향도 추가
    cur_node = c
    cur_parent = parent[c]
    cur_author = authority[c]

    # 자신의 영향 추가
    while (cur_author != 0) and (cur_parent != -1) and (m_status[cur_node]):
        messenger[cur_parent][cur_author - 1] += 1

        cur_node = cur_parent
        cur_parent = parent[cur_parent]
        cur_author -= 1

    # 자신 밑으로부터의 영향 추가
    for idx, val in enumerate(messenger[c]):
        if not val:
            continue

        cur_node = c
        cur_parent = parent[c]
        cur_author = idx

        # 자신의 영향 추가
        while (cur_author != 0) and (cur_parent != -1) and (m_status[cur_node]):
            messenger[cur_parent][cur_author - 1] += val

            cur_node = cur_parent
            cur_parent = parent[cur_parent]
            cur_author -= 1

    m_status[c] = 1

    return


def order200(c):
    # 알림망 설정 on -> off
    if m_status[c]:
        on_2_off(c)

    # 알림망 설정 off -> on
    else:
        off_2_on(c)

    return


def order300(c, power):
    # 기존 자신의 영향도 없앰
    if m_status[c]:
        cur_node = c
        cur_parent = parent[c]
        cur_author = authority[c]

        # 자신의 영향 없앰
        while (cur_author != 0) and (cur_parent != -1) and (m_status[cur_node]):
            messenger[cur_parent][cur_author - 1] -= 1

            cur_parent = parent[cur_parent]
            cur_author -= 1


    # 권한 세기 변경
    authority[c] = power

    # 자신의 영향 추가
    if m_status[c]:
        cur_node = c
        cur_parent = parent[c]
        cur_author = power

        while (cur_author != 0) and (cur_parent != -1) and (m_status[cur_node]):
            messenger[cur_parent][cur_author - 1] += 1

            cur_parent = parent[cur_parent]
            cur_author -= 1

    return

def order400(c1, c2):
    flag1 = flag2 = False

    # 각자 자신의 영향도 없앰
    if m_status[c1]:
        flag1 = True
        on_2_off(c1)
    if m_status[c2]:
        flag2 = True
        on_2_off(c2)

    # 부모 관계 변경
    bef_p1, bef_p2 = parent[c1], parent[c2]
    parent[c1], parent[c2] = bef_p2, bef_p1

    # 영향도 추가
    if flag1:
        off_2_on(c1)
    if flag2:
        off_2_on(c2)

    return

def order500(c):
    answer.append(sum(messenger[c]))

    return


N, Q = map(int, input().split())

answer = []
for _ in range(Q):
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
