"""
[SW Expert Academy 29717] 쥐를 잡자 쥐를 잡자 치치치
https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD6YOoqdaLHBISc&categoryId=AaD6YOoqdaLHBISc&categoryType=CODE

작성자 : @onyou-sub
결과   : 통과
"""


from collections import deque


def move():
    for i in range(1, C+1):
        if mouse[i] is None: # 죽은 쥐
            continue

        mr, mc = mouse[i]
        if matrix[mr][mc] > 0: # 이미 해당 위치 낙엽
            continue

        visited = [[0] * N for _ in range(N)]
        q = deque([(mr, mc, None)])
        visited[mr][mc] = 1
        nmr, nmc = -1, -1

        while q:
            cr, cc, first = q.popleft()

            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                    continue

                if (nr == chr and nc == chc) or mouse_grid[nr][nc]: # 치치 있거나 쥐 있음
                    continue

                if matrix[nr][nc] > 0: # 낙엽 찾음
                    nmr, nmc = first if first else (nr, nc)
                    break

                q.append((nr, nc, first if first else (nr, nc)))
                visited[nr][nc] = 1

            if nmr != -1: # 쥐 위치 이동
                mouse[i] = (nmr, nmc)
                mouse_grid[mr][mc] = 0  # 이전 위치 삭제
                mouse_grid[nmr][nmc] = i
                break


def chichi():
    if mouse_grid[chr][chc]: # 치치 위치에 쥐 있으면
        return chr, chc

    visited = [[0] * N for _ in range(N)]
    q = deque([(chr, chc, None)])
    visited[chr][chc] = 1
    maxr, maxc = -1, -1 # 가장 가까운 쥐. 행큰 열큰
    nchichi = None # 치치 다음 위치

    while q:
        for _ in range(len(q)):
            cr, cc, first = q.popleft()

            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if visited[nr][nc] or matrix[nr][nc] == -1:  # 돌 못감
                    continue

                if mouse_grid[nr][nc]:
                    if (maxr, maxc) < (nr, nc):
                        maxr, maxc = nr, nc
                        nchichi = first if first else (nr, nc)
                else:
                    q.append((nr, nc, first if first else (nr, nc)))
                    visited[nr][nc] = visited[cr][cc] + 1

        if maxr != -1: # 가장 가까운 애
            return nchichi

    # 다 돌았는데도 없으면 지금 위치
    return chr, chc


T = int(input())

dr = [-1, 0, 1, 0] # 상우하좌
dc = [0, 1, 0, -1]

for tc in range(1, T+1):
    N, C, D = map(int, input().split()) # 격자 크기, 쥐 개수, 일 수. 50, 50, 100
    matrix = [list(map(int, input().split())) for _ in range(N)] # 0 = 빈칸, -1 = 돌, 1-100 = 낙엽
    chr, chc = (int(x)-1 for x in input().split()) # 치치 위치
    mouse = [None] # 1번부터
    mouse_grid = [[0] * N for _ in range(N)] # 번호 표시
    caught = [] # 잡힌 쥐 번호 저장
    ans = -1 # 쥐 다 잡은 일 수

    for i in range(1, C+1):
        r, c = (int(x)-1 for x in input().split())
        mouse.append((r, c))
        mouse_grid[r][c] = i

    for day in range(1, D+1):
        # 1. 낮 치치 이동
        chr, chc = chichi()

        if mouse_grid[chr][chc] and matrix[chr][chc] == 0: # 쥐 있고 낙엽 없으면 잡기
            idx = mouse_grid[chr][chc] # 쥐 번호
            mouse[idx] = None # 죽음
            caught.append(idx)
            mouse_grid[chr][chc] = 0

        # 쥐 다 잡으면 끝
        if len(caught) == C:
            ans = day
            break

        # 2. 밤 쥐 이동
        move()

        # 3. 낙엽 확산
        new_matrix = [row[:] for row in matrix]

        for i in range(N):
            for j in range(N):
                if matrix[i][j]//5 > 0: # 확산될 낙엽 있으면
                    spread = matrix[i][j] // 5

                    for d in range(4):
                        nr = i + dr[d]
                        nc = j + dc[d]

                        if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] == 0): # 빈칸만
                            continue

                        new_matrix[nr][nc] += spread
                        new_matrix[i][j] -= spread

        matrix = new_matrix

        # 4. 낙엽 -5
        for i in range(N):
            for j in range(N):
                if matrix[i][j] > 0: # 낙엽 있는 경우만
                    matrix[i][j] = max(matrix[i][j]-5, 0)

    # 일 수, 잡힌 쥐 번호. 못 잡으면 -1
    print(f'#{tc}', ans, *caught if ans != -1 else '')
