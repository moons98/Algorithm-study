# -*- coding: utf-8 -*-
import sys

N = int(sys.stdin.readline())
graph = [int(sys.stdin.readline()) - 1 for _ in range(N)]  # 0부터 시작하도록 맞춰줌

answer = []
for i in range(N):
    temp = i
    for _ in range(N):
        if graph[temp] == i:
            answer.append(i)  # 자기 자신을 가리키는 경우
            break
        temp = graph[temp]  # 둘째 열에 해당하는 index 찾아가서 비교

print(len(answer))
for num in answer:
    print(num + 1)

"""
[0 1 2 3 4 5]
[3 0 1 1 5 6]

1. [0,3]에서 3번째로 감
2. [3,1]에 해당하는 1번째로 감
3. [1,0]에 0으로 돌아왔으니 0 추가
"""
