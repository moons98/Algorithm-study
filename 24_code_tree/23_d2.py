'''
코드트리 오마카세

start: 00:50
end: 02:05

회고 :
    - 단순 쿼리 처리하는 문제
    - 초밥을 먹는 액션과 손님이 사라지는 액션이 명확하게 계산됨
    - 따라서 해당 과정도 쿼리로 처리함

    - 손님이 사라지는 타이밍을 max로 관리해야 나중 초밥 먹는 시간으로 덮어쓰기가 되지 않음



- 원형 형태의 초밥 벨트와 L개의 의자
- x=0부터 시계 방향으로 x=L-1까지 회전
- 1초에 한 칸씩 시계 방향으로 회전

(1) 주방장의 초밥 만들기
    - 시각 t에 위치 x 앞에 name 이름을 부탁한 초밥 올려 놓음
    - 초밥 회전이 일어난 직후 발생
    - 같은 위치에 여러 초밥 존재 가능

(2) 손님 입장
    - 이름이 name인 사람이 시각 t에 위치 x에 입장
    - 회전이 일어난 직후에 발생
    - 위치 x 앞으로 오는 초밥들 중 자신의 이름이 적힌 초밥을 n개 먹고 자리를 떠남
    - 착석 즉시 먹을 수 있음, 여러 개도 먹을 수 있음

(3) 사진 촬영
    - 시각 t에 가게 모습 촬영
    - 초밥 회전 -> 손님 입장 및 식사 -> 사진 촬영 순서
    - 가게에 남은 사람 수와 남은 초밥 수 출력

'''
from collections import defaultdict

def order100(t, x, name):
    t, x = map(int, [t, x])

    # 만약 사람이 없다면
    if name not in people.keys():
        people_sushi[name].append([t, x])
    # 사람이 있다면, 없어지는 시간도 넣어줌
    else:
        # 현재 시간 + (사람-스시)%L
        time = t + ((people[name][0] - x) % L)
        query.append([201, time])

        # 사람이 먹는 스시 수 체크
        people[name][1] -= 1
        people[name][2] = max(time, people[name][2])
        if people[name][1] == 0:
            query.append([202, people[name][2]])

    return

def order200(t, x, name, n):
    t, x, n = map(int, [t, x, n])

    # 위치, 먹는 갯수, 마지막 먹은 시간
    people[name] = [x, n, -1]

    # 만약 초밥이 이미 존재한다면
    for _t, _loc in people_sushi[name]:
        cur_sushi_loc = ((t - _t) + _loc) % L
        time = t + ((x - cur_sushi_loc) % L)

        query.append([201, time])

        # 사람이 먹는 스시 수 체크
        people[name][1] -= 1
        people[name][2] = max(time, people[name][2])
        if people[name][1] == 0:
            query.append([202, people[name][2]])

    return


L, Q = map(int, input().split())

# 사람 정보, 사람-초밥 정보
people = dict()
people_sushi = defaultdict(lambda:[])

query = []
for q in range(Q):
    order, *tmp = input().split()
    query.append([int(order), int(tmp[0])])

    if int(order) == 100:
        order100(*tmp)
    elif int(order) == 200:
        order200(*tmp)

# 시간 순서대로 정렬
query.sort(key= lambda x:(x[1], x[0]))

num_sushi, num_people, answer = 0, 0, []
for order, t, *tmp in query:
    if order == 100:
        num_sushi += 1
    elif order == 200:
        num_people += 1
    elif order == 201:
        num_sushi -= 1
    elif order == 202:
        num_people -= 1
    elif order == 300:
        answer.append((num_people, num_sushi))

for people, sushi in answer:
    print(f'{people} {sushi}')
