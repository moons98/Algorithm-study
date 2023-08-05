# -*- coding: utf-8 -*-
import sys
from collections import deque


def can_make(word1, word2):
    ret = False
    for i in range(len(word2)):
        if word2[:i] + word2[i + 1 :] == word1:
            ret = True
    return ret


def bfs(queue, answer):
    while queue:
        word, tmp_len = queue.popleft()
        for i in word_snippet:
            # print(word, i, can_make(word, i))
            if len(i) == tmp_len + 1 and can_make(word, i):
                queue.append([i, tmp_len + 1])
                answer = i
                if len(answer) == len(word_snippet[-1]):
                    return answer
    return answer


d, _word = sys.stdin.readline().split()
word_snippet = [sys.stdin.readline().rstrip() for _ in range(int(d))]
word_snippet.sort(key=lambda x: len(x))

queue = deque()
queue.append([_word, len(_word)])
answer = _word

print(bfs(queue, answer))


"""
Counter로 바꿔서 문자 찾고 위치에 추가하는 과정 없이, 그냥 한 글자를 떼고 더했을 때 원본과 같은 지 판단해야 시간초과 안남
"""
