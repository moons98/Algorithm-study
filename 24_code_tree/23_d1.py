'''
start: 21:25
end : 23:35

회고 :
    - 산타가 없는 즉시 게임이 끝남 -> flag로 했는지 해설 확인
    - 기절은 최대 2까지만 가능함
    - 진행 중에 산타가 사라졌을 수도 있음 -> 산타 idx를 list로 풀어서 관리했는데 해설은 어떻게 했는지 확인 필요

P명의 산타

1. 게임판의 구성
    - NxN 격자, (r,c), 좌상단은 (1,1)
    - M개의 턴에 걸쳐 진행
    - 루돌프가 한 번 움직인 뒤, 1~P번의 산타가 순서대로 움직임
    - 기절하거나 격자 밖으로 빠져나가 탈락한 산타는 움직이지 못함
    - 거리는 L2-norm

2. 루돌프의 움직임
    - 가장 가까운 산타를 향해 한 칸 돌진
        - 게임에서 탈락하지 않은 산타 중 가까운 산타를 선택
        - 두 명 이상일 경우, r이 큰 >> c가 큰 우선순위
        - 루돌프는 상하좌우 및 대각선으로 돌진 가능

3. 산타의 움직임
    - 1~P번까지 순서대로 움직임
    - 기절 or 탈락한 산타는 움직이지 못함
    - 루돌프에게 거리가 가까워지는 방향으로 한 칸 이동
    - 다른 산타가 있는 칸으로 움직이지 못함
    - 움직일 수 있는 칸이 없다면 움직이지 않음
    - 있더라도, 루돌프로부터 가까워질 수 없다면 움직이지 않음
    - 상하좌우 네 방향 중 하나로 움직일 수 있음
    - 두 개 이상이라면, 상 >> 우 >> 하 >> 좌 순서

4. 충돌
    - 산타와 루돌프가 같은 칸이면 충돌
    - 루돌프의 움직임으로 충돌
        - 산타는 C만큼 점수 획득
        - 루돌프가 이동해온 방향으로 C칸 밀려남
        - 이동하는 도중에 충돌 x
        - 밀려난 위치가 밖이라면 탈락, 다른 산타가 있으면 상호작용
    - 산타의 움직임으로 충돌
        - 산타는 D만큼의 점수를 얻음
        - 자신이 이동한 반대 방향으로 D칸 만큼 밀려남

5. 상호작용
    - 루돌프의 충돌 후 다른 산타와 만나면, 그 산타는 해당 방향으로 한 칸 밀려남
    - 연쇄적으로 밀려나는 것을 반복

6. 기절
    - 산타는 루돌프와 충돌 후 기절
    - k+2번째 턴부터 다시 정상상태
    - 기절한 산타는 움직이지 못함, 상호작용이나 충돌로 밀려날 수는 있음
    - 루돌프는 기절한 산타를 돌진 상태로 선택 가능

7. 게임 종료
    - M번의 턴에 걸쳐 순서대로 움직이고 종료
    - 산타가 모두 탈락 -> 즉시 종료
    - 매 턴 이후 탈락하지 않은 산타는 1점씩 추가 부여

각 산타가 얻은 최종 점수
'''

def collide(x, y, _dx, _dy, s, d):
    idx = map_lst[x][y]

    # 점수 획득
    score[idx] += s

    # score만큼 획득, distance만큼 밀려남
    map_lst[x][y] = 0

    nx, ny = x + _dx*d, y + _dy*d
    # 만약 격자 밖일 경우 탈락
    if nx < 0 or nx >= N or ny < 0 or ny >= N:
        santa.pop(idx)
        stun.pop(idx)
        return

    # 순차적 밀려남
    if map_lst[nx][ny]:
        collide(nx, ny, _dx, _dy, 0, 1)

    # 새로운 위치 등록
    map_lst[nx][ny] = idx
    santa[idx] = (nx, ny)

    return


def move_rudolf():
    global rudolf

    rx, ry = rudolf
    distance = (50**2) * 2

    # 가장 가까운 산타 찾기, 거꾸로 (좌표:번호) 순서
    targets = dict()
    for idx, (x, y) in santa.items():
        new_distance = abs(x - rx)**2 + abs(y - ry)**2

        if new_distance < distance:
            distance = new_distance
            targets = {(x,y):idx}
        elif new_distance == distance:
            distance = new_distance
            targets[(x,y)] = idx

    locs = list(targets.keys())
    locs.sort(key=lambda x:(-x[0],-x[1]))

    # 우선순위 가장 큰 산타
    (sx, sy), t_idx = locs[0], targets[locs[0]]

    # 이동 방향
    if rx > sx:
        t_dx = -1
    elif rx == sx:
        t_dx = 0
    else:
        t_dx = 1

    if ry > sy:
        t_dy = -1
    elif ry == sy:
        t_dy = 0
    else:
        t_dy = 1

    # 원래 위치 없애줌
    map_lst[rx][ry] = 0

    nx, ny = rx + t_dx, ry + t_dy
    if map_lst[nx][ny]:
        stun[t_idx] = 2
        collide(nx, ny, t_dx, t_dy, C, C)


    # 새로운 위치 등록
    map_lst[nx][ny] = -1
    rudolf = (nx, ny)

    return


def move_santa(idx):
    if idx not in santa.keys():
        return
    # 기절 상태일 경우
    elif stun[idx]:
        return 

    rx, ry = rudolf
    sx, sy = santa[idx]

    # 움직이는 방향 찾기
    distance, d = abs(rx - sx)**2 + abs(ry - sy)**2, -1
    for i in range(4):
        nx, ny = sx + dx[i], sy + dy[i]

        if nx < 0 or nx >= N or ny < 0 or ny >= N:
            continue
        # 다른 산타를 만나는 경우
        elif map_lst[nx][ny] > 0:
            continue

        cur_distance = abs(rx - nx)**2 + abs(ry - ny)**2
        if cur_distance < distance:
            distance = cur_distance
            d = i

    # 움직일 수 없다면 생략
    if d == -1:
        return

    # 현 위치에서 제거
    map_lst[sx][sy] = 0

    nx, ny = sx + dx[d], sy + dy[d]

    # 루돌프를 만나는 경우
    if map_lst[nx][ny] == -1:
        # collide 들어 가기 위해 위치 등록
        map_lst[nx][ny] = idx

        # 스턴
        stun[idx] = 2

        # 진행해온 반대 방향으로 튕겨나감
        nd = (d + 2) % 4
        collide(nx, ny, dx[nd], dy[nd], D, D)

        # 루돌프 위치 재등록
        map_lst[nx][ny] = -1
    # 재등록
    else:
        map_lst[nx][ny] = idx
        santa[idx] = (nx, ny)

    return


def add_score():
    for idx, _ in santa.items():
        score[idx] += 1

    return


# NxN, M턴, P명 산타, C칸, D칸
N, M, P, C, D = map(int, input().split())

map_lst = [[0 for _ in range(N)] for _ in range(N)]

r, c = map(int, input().split())
rudolf = (r-1, c-1)

# 루톨프는 -1로 표시
map_lst[r-1][c-1] = -1

santa = dict()
score = dict()
stun = dict()
for _ in range(P):
    i, r, c = map(int, input().split())
    santa[i] = (r-1, c-1)
    map_lst[r-1][c-1] = i

    score[i] = 0
    stun[i] = 0


# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

flag = True
for _ in range(M):
    move_rudolf()
    if not santa:
        break

    santa_idx = list(santa.keys())
    santa_idx.sort()
    for idx in santa_idx:
        move_santa(idx)
        if not santa:
            flag = False
            break
    if not flag:
        break

    add_score()

    # 기절 스택 줄이기
    for idx, val in stun.items():
        stun[idx] = max(0, val -1)


score_idx = list(score.keys())
score_idx.sort()
for idx in score_idx:
    print(score[idx], end=' ')