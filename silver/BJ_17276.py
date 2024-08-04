# import sys
# sys.stdin = open("../input.txt", "r")


'''
대응 축만 만들면 해결됨

4개의 축을 돌려야 함
한 축 당 n개의 원소 존재
'''


import copy

T = int(input())

def print_map(map_lst):
    for i in map_lst:
        print(*i)
    # print()

    return


for _ in range(T):
    n, d = map(int, input().split())
    d = (d % 360) // 45

    loc_set = [[(x, x) for x in range(n)], [(x, n//2) for x in range(n)], [(x, n-1-x) for x in range(n)], [(n//2, n-1-x) for x in range(n)]]

    # ori_map
    map_lst = [list(map(int, input().split())) for i in range(n)]
    new_map = copy.deepcopy(map_lst)

    # rotate
    # per axis
    for i in range(4):
        axis_set = loc_set[i]

        # axis num increases
        nd  = (d + i) % 8

        # per element
        for j in range(n):
            [x, y] = axis_set[j]

            # normal order
            if nd < 4:
                [nx, ny] = loc_set[nd][j]
            # reverse order
            else:
                [nx, ny] = loc_set[nd-4][n - 1 - j]

            new_map[nx][ny] = map_lst[x][y]

        # print_map(new_map)

    map_lst = new_map
    print_map(map_lst)


'''
1
5 45
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25

1
5 -45
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25

1
5 135
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25

1
5 360
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25
'''