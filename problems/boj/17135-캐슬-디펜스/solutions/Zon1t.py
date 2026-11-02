"""
[Baekjoon 17135] 캐슬 디펜스
https://sorryday.tistory.com/95

작성자 : @Zon1t
결과   : 통과 / 실패 (실행 시간 ms, 메모리 KB)
복잡도 : (선택) 시간 O( ), 공간 O( )
접근   :
    - itertools 써도 되고.. 나는 그냥 백트래킹으로 궁수의 위치를 잡아주었다.
    - 우선 순위에 의거한 대상을 잡아, 중복을 적절하게 처리해주었다.
회고   :
    - 그냥 델타 리스트 만들어서 우선 순위를 판별하는 편이 더 좋았을 것 같다.
"""


import sys
input = sys.stdin.readline
from collections import deque

dr = [0, -1, 0]
dc = [-1, 0, 1]

def in_range(row, col):
    return (0 <= row < N and 0 <= col < M)

def find_target(bow_master, duplicated_grid):
    visited = [[False] * M for _ in range(N)]
    visited[N-1][bow_master] = True
    q = deque([(N-1, bow_master, 1)])
    while q:
        row, col, d = q.popleft()
        if duplicated_grid[row][col] == 1:
            return (row, col)
        for i in range(3):
            nr, nc = row+dr[i], col+dc[i]
            if not in_range(nr, nc) or visited[nr][nc]:
                continue
            if d < D:
                q.append((nr, nc, d+1))
                visited[nr][nc] = True
    return False

def is_enemy(duplicated_grid):
    for row in range(N):
        for col in range(M):
            if duplicated_grid[row][col] == 1:
                return True
    return False

def simulate(pos_bowmasters):
    duplicated_grid = [row[:] for row in grid]
    count = 0
    while is_enemy(duplicated_grid):
        enemy_set = set()
        for bow_master in pos_bowmasters:
            target = find_target(bow_master, duplicated_grid)
            if target:
                enemy_set.add(target)
        for row, col in enemy_set:
            duplicated_grid[row][col] = 0
            count += 1
        for row in range(N-1, 0, -1):
            for col in range(M):
                duplicated_grid[row][col] = duplicated_grid[row-1][col]
        for col in range(M):
            duplicated_grid[0][col] = 0

    return count

def backtrack(cnt, start, temp_list):
    if cnt == 3:
        combination_list.append(temp_list[:])
        return
    for i in range(start, M):
        temp_list.append(i)
        backtrack(cnt+1, start+1, temp_list)
        temp_list.pop()

N, M, D = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
combination_list = []
max_number = 0
backtrack(0, 0, [])

for pos_bowmasters in combination_list:
    count = simulate(pos_bowmasters)
    if max_number < count:
        max_number = count
print(max_number)