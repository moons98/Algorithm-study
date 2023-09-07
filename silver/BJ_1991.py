# -*- coding: utf-8 -*-
import sys
from collections import deque


N = int(sys.stdin.readline())
graph = dict()

for i in range(N):
    tmp, left, right = map(str, sys.stdin.readline().strip().split())
    graph[tmp] = [left, right]


def preorder(node):
    if node != ".":
        print(node, end="")
        preorder(graph[node][0])
        preorder(graph[node][1])


def inorder(node):
    if node != ".":
        inorder(graph[node][0])
        print(node, end="")
        inorder(graph[node][1])


def postorder(node):
    if node != ".":
        postorder(graph[node][0])
        postorder(graph[node][1])
        print(node, end="")


preorder("A")
print()
inorder("A")
print()
postorder("A")
print()

"""
node 순서가 마음대로니까 dict type으로 저장
https://velog.io/@ohk9134/%EB%B0%B1%EC%A4%80-1991%EB%B2%88-%ED%8A%B8%EB%A6%AC-%EC%88%9C%ED%9A%8C-python-%ED%8A%B8%EB%A6%AC-%EA%B5%AC%ED%98%84
"""
