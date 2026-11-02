"""
[Programmers 169199] 리코쳇 로봇
https://school.programmers.co.kr/learn/courses/30/lessons/169199?gad_source=1&gad_campaignid=22356298761&gbraid=0AAAAAC_c4nDtlcqqydkNIAku5Cjs5iSfH&gclid=CjwKCAjwgJHXBhBGEiwAHohJq406kxXLW-M40qmcT3QjVvQFHThL-44RXSt1hphACQnUZLnMrtAzUhoCAU4QAvD_BwE

작성자 : @Hyunnniiii
결과   : 통과
접근   :
    - BFS 템플릿 그대로 사용하는데, 큐에는 지나간 모든 좌표가 아니라 멈춘 좌표 & 이동횟수 넣어줬다.
회고   :
    - 그냥 BFS인 것만 알아채면 쉬운 문제같음.
"""

from collections import deque

def solution(board):
    R, C = len(board), len(board[0])

    # 시작점 찾기
    for i in range(R):
        for j in range(C):
            if board[i][j] == 'R':
                sr, sc = i, j

    visit = [[False] * C for _ in range(R)]
    visit[sr][sc] = True

    Q = deque()
    Q.append((sr, sc, 0))   # (행, 열, 이동 횟수)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상하좌우

    while Q:
        r, c, cnt = Q.popleft()

        # 목적지 도착
        if board[r][c] == 'G':
            return cnt

        for dr, dc in directions:
            nr, nc = r, c

            # 장애물이나 벽을 만날 때까지 이동
            while (0 <= nr + dr < R and 0 <= nc + dc < C and
                   board[nr + dr][nc + dc] != 'D'):
                nr += dr
                nc += dc

            # 멈춘 위치를 큐에 추가
            if not visit[nr][nc]:
                visit[nr][nc] = True
                Q.append((nr, nc, cnt + 1))

    # 도착 못하면
    return -1


