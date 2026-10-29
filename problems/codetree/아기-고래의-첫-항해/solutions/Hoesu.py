"""
[Codetree baby-whale-first-voyage] 아기 고래의 첫 항해
https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/baby-whale-first-voyage

작성자 : @Hoesu
결과   : 통과 / 실패 (실행 시간 ms, 메모리 KB)
복잡도 : 시간 O( ), 공간 O( )
접근   :
  -
  -
회고   :
  -
"""


from collections import deque


def debug(msg):
    print()
    print(msg)
    for x in ocean:
        print(*x)
    print()
    for x in visit:
        print(*x)
    print('---')


def move(cr, cc, cd):
    for delta in [0, 1, -1, 2]:
        nd = (cd + delta) % 4
        nr = cr + DR[nd]
        nc = cc + DC[nd]

        if not(0 <= nr < N and 0 <= nc < N):
            continue
        if ocean[nr][nc] == 1:
            continue
        if visit[nr][nc] != 0:
            continue
        visit[nr][nc] = visit[cr][cc]+1
        return nr, nc, nd
    return None, None, None


def find_ocean(sr, sc, sd):
    que = deque()
    que.append((sr, sc, sd))
    vst = [[0] * N for _ in range(N)]
    vst[sr][sc] = 1

    threshold = N**3
    candidates = []

    while que:
        cr, cc, cd = que.popleft()
        if vst[cr][cc] > threshold:
            break
        if visit[cr][cc] == 0:
            threshold = vst[cr][cc]
            candidates.append((cr, cc, cd, vst[cr][cc]))

        for i in range(4):
            nr = cr + DR[i]
            nc = cc + DC[i]
            nd = i

            if not (0 <= nr < N and 0 <= nc < N):
                continue
            if vst[nr][nc] != 0:
                continue
            if ocean[nr][nc] == 1:
                continue
            vst[nr][nc] = vst[cr][cc]+1
            que.append((nr, nc, nd))

    if not candidates:
        return None, None, None
    candidates.sort(key=lambda x: (x[3], x[0], x[1]))
    fr, fc, fd, _ = candidates[0]
    visit[fr][fc] = visit[sr][sc] + 1
    return fr, fc, fd


if __name__ == '__main__':
    DR = (0, 1, 0, -1)
    DC = (-1, 0, 1, 0)
    adapter = [3, 1, 0, 2]

    N, R, C, D = map(int, input().split())
    ocean = [list(map(int, input().split())) for _ in range(N)]
    visit = [[0] * N for _ in range(N)]

    Wr, Wc, Wd = R-1, C-1, adapter[D-1]
    trajectory = [(Wr, Wc)]
    visit[Wr][Wc] = 1

    while True:

        # TODO 1: 인접 이동
        while True:
            nWr, nWc, nWd = move(Wr, Wc, Wd)
            if nWd is None:
                break
            else:
                Wr, Wc, Wd = nWr, nWc, nWd
                trajectory.append((Wr, Wc))

        # TODO 2: 가장 가까운 바다 이동
        nWr, nWc, nWd = find_ocean(Wr, Wc, Wd)
        if nWd is None:
            break
        else:
            Wr, Wc, Wd = nWr, nWc, nWd
            trajectory.append((Wr, Wc))

    # 정답 출력
    for r, c in trajectory:
        print(r+1, c+1)
