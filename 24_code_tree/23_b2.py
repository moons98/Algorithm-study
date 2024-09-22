'''
코드트리 채점기

start: 22:00
end: 00:42

회고 :
    - heapq을 domain별로 관리하지 않아서 시간초과 발생
    - NlogN으로 해결해야 했던 문제임;;

(1) 코드트리 채점기 준비
    - N개의 채점기 준비, 초기 문제 url에 해당하는 u0가 주어짐
    - url은 도메인/문제id 형태
    - 도메인은 알파벳 소문자와 '.'으로 구성, 문제 ID는 1이상 10억 이하의 정수값
    - N개의 채점기에는 1~N번까지의 번호가 붙음
    - 0초에 채점 우선순위가 1이면서 url이 u0인 문제에 대한 채점 요청이 들어옴
    - 채점 task는 채점 대기 큐에 들어감

(2) 채점 요청
    - t초에 채점 우선순위가 p이면서 url이 u인 문제에 대한 채점 요청이 들어옴
    - task는 채점 대기 큐에 들어감
    - 채점 대기 큐의 task 중 정확히 u와 일치하는 url이 존재한다면 큐에 추가하지 않음

(3) 채점 시도
    - t초에 큐에서 즉시 채점이 불가능한 경우를 제외하고 남은 task 중 우선순위가 가장 높은 채점 task를 골라 채점 진행
    - 채점이 될 수 없는 조건
        - 해당 task의 도메인이 현재 채점을 진행중인 도메인 중 하나
        - 해당 task의 도메인과 일치하는 도메인에 대해 최근에 진행한 재점 시작이 start, 종료 시간이 start + gap
            - 현재 시간이 (start + 3*gap)보다 작으면 채점 불가
    - 채점 우선순위
        - 우선순위 p의 번호가 작을수록
        - 채점 대기 큐에 들어온 시간이 빠를수록
    - 채점이 가능한 task가 하나라도 있으면 쉬고 있는 채점기 중 번호가 가장 작은 채점기가 채점 시작
    - 쉬고 있는 채점기가 없다면 요청 무시하고 넘어감

(4) 채점 종료
    - t초에 J_id번 채점기가 진행하던 채점이 종료, 다시 쉬는 상태
    - 진행하던 채점이 없었다면 명령 무시

(5) 채점 대기 큐 조회
    - 채점 대기 큐에 있는 채점 task의 수 출력

'''
import copy
import heapq

class Task:
    def __init__(self, id, p, t):
        self.id = id
        self.p = p
        self.t = t

    def __gt__(self, other):
        if self.p != other.p:
            return self.p > other.p
        elif self.t != other.t:
            return self.t > other.t


def order100(N, u0):
    global waiting_checker, working_checker

    # 채점기 정보
    waiting_checker = [i for i in range(1, int(N)+1)]
    working_checker = dict()

    heapq.heapify(waiting_checker)
    
    # url=u0인 문제 들어옴
    order200(0, 1, u0)

    return


def order200(t, p, u):
    t, p = map(int, [t, p])

    domain, id = u.split('/')

    # u와 일치하는 url이 없다면
    if (domain in task_queue.keys()):
        for _task in task_queue[domain]:
            if _task.id == id:
                return
    else:
        task_queue[domain] = []

    heapq.heappush(task_queue[domain], Task(id, p, t))

    return


def order300(t):
    t = int(t)

    # 채점 가능한 checket가 있는 지 확인
    if not waiting_checker:
        return

    target_domain = None
    target_task = None

    # 채점 가능한 task가 있는 지 확인, 채점 불가능한 domain은 통째로 날림
    for _domain, task_lst in task_queue.items():
        # 빈 lst skip
        if not task_lst:
            continue

        if (_domain in checking_lst.keys()):
            # 채점 중인 도메인
            if checking_lst[_domain][1] == -1:
                continue

            # 현재 시간이 (start + 3*gap)보다 작으면 불가능
            start = checking_lst[_domain][0]
            end = checking_lst[_domain][1]

            if (end == -1) or (t < start + (end - start) * 3):
                continue

        # 각 도메인 별 돌면서 가장 우선 순위 높은 task 찾기
        if not target_domain:
            target_domain = _domain
            target_task = task_lst[0]
        elif task_lst[0] < target_task:
            target_domain = _domain
            target_task = task_lst[0]

    # 채점 가능한 task가 있다면
    if target_task:
        _ = heapq.heappop(task_queue[target_domain])

        start, end = t, -1

        # 채점기 정보 갱신
        target_checker = heapq.heappop(waiting_checker)
        working_checker[target_checker] = target_domain

        # domain 채점 중 갱신
        checking_lst[target_domain] = [start, end]

    return


def order400(t, J_id):
    t, J_id = map(int, [t, J_id])

    # 진행하던 채점이 없었다면 무시
    if J_id not in working_checker.keys():
        return

    # 채점기 대기 상태로 변경
    _domain = working_checker.pop(J_id)
    heapq.heappush(waiting_checker, J_id)

    # domain 정보에 끝남 체크
    checking_lst[_domain][1] = t

    return


def order500(t):
    t = int(t)

    cur_answer = sum(len(i) for i in task_queue.values())
    answer.append(cur_answer)

    return


Q = int(input())

# 채점 중 정보 {domain: [start, gap]}
checking_lst = dict()

# 채점 대기 큐, Task class로 관리 (p 작을수록 << t 작을수록, 같은 url 없어야 함)
# domain마다 우선순위 큐 유지
task_queue = dict()

answer = []
for _ in range(Q):
    order, *tmp = input().split()

    if order == '100':
        order100(*tmp)
    elif order == '200':
        order200(*tmp)
    elif order == '300':
        order300(*tmp)
    elif order == '400':
        order400(*tmp)
    elif order == '500':
        order500(*tmp)

for i in answer:
    print(i)
