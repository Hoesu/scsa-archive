"""
[Baekjoon 1194] 달이 차오른다, 가자.
https://nahwasa.com/entry/%EC%9E%90%EB%B0%94-%EB%B0%B1%EC%A4%80-1194-%EB%8B%AC%EC%9D%B4-%EC%B0%A8%EC%98%A4%EB%A5%B8%EB%8B%A4-%EA%B0%80%EC%9E%90-java

작성자 : @Zon1t
결과   : 통과 / 실패 (실행 시간 ms, 메모리 KB)
복잡도 : (선택) 시간 O( ), 공간 O( )
접근   :
    - 열쇠가 6개, N과 M이 50이하.. 열쇠 소지 조합 개수만큼 방문 배열을 생성하면 되겠다고 판단
    - 좌표값과 함께 열쇠 조합에 대한 값을 통해 큐에 집어넣으며 bfs 진행
회고   :
    - 열쇠를 중복해서 먹으러 가는 경우에 대한 적절한 처리 등 적잖게 생각할 부분이 많았다.
"""


'''
key를 가지게 되었을 때 중복처리 잘하기
distance를 따로 저장해서 사용하기(visited의 역할도 같이 하게 된다.)
'''

from collections import deque

def in_range(row, col):
    return (0 <= row < N and 0 <= col < M)

def check_key(key, door):
    need_key = ord(door) - ord('A')
    return key&(1<<need_key)

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

N, M = map(int, input().split())
grid = [input().strip() for _ in range(N)]
distance = [[[-1]*M for _ in range(N)] for _ in range(64)]

find = False
start_row, start_col = -1, -1
for row in range(N):
    for col in range(M):
        if grid[row][col] == '0':
            distance[0][row][col] = 0
            start_row, start_col = row, col
            find = True
            break
    if find: break

q = deque([(start_row, start_col, 0)])
while q:
    row, col, key = q.popleft()
    d = distance[key][row][col]
    if grid[row][col] == '1':
        print(d)
        exit(0)
    
    for i in range(4):
        nr, nc = row + dr[i], col + dc[i]
        if not in_range(nr, nc):
            continue
        if grid[nr][nc] == '#':
            continue
        if distance[key][nr][nc] != -1:
            continue

        if 'a' <= grid[nr][nc] <= 'f':
            temp_key = 1<<(ord(grid[nr][nc])-ord('a'))
            if key&temp_key:
                temp_key = key
            else:
                temp_key += key
                
            distance[temp_key][nr][nc] = d+1
            q.append((nr, nc, temp_key))
            continue

        if 'A' <= grid[nr][nc] <= 'F' and not check_key(key, grid[nr][nc]):
            continue
        distance[key][nr][nc] = d+1
        q.append((nr, nc, key))
print(-1)