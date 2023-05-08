# -*- coding: utf-8 -*- 
import re
import sys

T = int(input())
results = []

for _ in range(T):
    sign = sys.stdin.readline().replace('\n', '')
    p = re.compile('(100+1+|01)+')
    m = p.fullmatch(sign) # match 사용할 경우, 일부분만 일치하더라도 true로 반환
    if m: 
        results.append("YES")
    else: 
        results.append("NO")
        
for i in results:
    print(i)


'''
# 10011001에서 예외 발생
import sys

def find_zero(line):
    idx = line.find('0')
    return idx

def find_one(line):
    idx = line.find('1')
    return idx

answer = []                
def check_avail(idx):
    if idx == -1:
        answer.append('NO')
        return False
    
    return True
    
    
num = int(input())
for i in range(num):
    line = sys.stdin.readline()
    
    start, end = 0, len(line)-1
    while True:
        if line[start:].startswith('100'):
            start += 3
            #print(line[start:])
            # 0 무리, 1 무리 한 번 지나가야 함
            idx = find_one(line[start:])
            if not check_avail(idx):
                break
            else:
                start += idx
                
            idx = find_zero(line[start:])
            if not check_avail(idx):
                answer[-1] = 'YES'
                break
            else:
                start += idx
                #print(line[start:])
        elif line[start:].startswith('01'):
            start += 2
            #print(line[start:])
        else:
            idx = -1
            check_avail(idx)
            break
        
        #print(line[start:], start, end)
        if start >= end:
            answer.append('YES')
            break
    
for i in answer:
    print(i)
'''