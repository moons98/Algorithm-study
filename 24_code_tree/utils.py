'''
coding-test 진행 중, 자주 사용되는 로직들을 모아 놓는 코드
'''

# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

n = 5
dir_forward = [[-1 for _ in range(n)] for _ in range(n)]
dir_reverse = [[-1 for _ in range(n)] for _ in range(n)]


def snail():
    '''
    11, 22, 33, 44 '4'의 형식으로 증가 -> 다음 방향이 '상' 혹은 '하'가 될 경우에 횟수 증가
    reverse 움직임은 forward 움직임과 역의 방향 -> %4로 바로 계산 가능
    while - break 구문 통해서 마지막 증가하지 않고 끝나는 숫자 컨트롤 -> (0,0)이 마지막 지점임이 자명함
    -1을 만나면 flag를 바꿔서 사용하면 됨
    '''
    x, y = (n//2, n//2)
    d, num_move = 0, 1

    while x or y:
        for _ in range(num_move):
            dir_forward[x][y] = d

            # 반대 움직임은 한 칸 움직인 후에 결정할 수 있음
            x, y = x + dx[d], y + dy[d]
            dir_reverse[x][y] = (d + 2) % 4
                
            # while 구문이 깨지는 조건과 같이 둬서 한 번에 꺠지도록 설정
            # 실제 값 전달은 위에서 하므로 아래에서 도는쪽은 결과에 영향 주지 않음
            if (not x) and (not y):
                break
        
        # 위치 증가
        d = (d + 1) % 4

        # 움직임 횟수 증가
        if d == 0 or d == 2:
            num_move += 1

    return





if __name__ == "__main__":
    snail()
