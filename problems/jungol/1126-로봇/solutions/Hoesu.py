"""
[JUNGOL 1126] 로봇
https://jungol.co.kr/problem/1126

작성자 : @Hoesu
결과   : 통과
접근   :
    - 모든 좌표를 2배로 확대해, 원래 두 격자점 사이의 중간점으로 선분이 장애물 내부를 관통하는지 판별
    - 각 L자 장애물을 오목 꼭짓점 p4와 나머지 세 점을 대각으로 하는 직사각형 3개의 합집합으로 격자에 표시
    - 8방향 이웃이 모두 같은 장애물인 점만 '내부'로 막고, 경계(변·꼭짓점)는 통과 가능하게 처리
    - 상태 (x, y, 방향)에 대해 직진은 비용 0, 방향 전환은 비용 1인 0-1 BFS로 최소 꺾임 횟수 계산
회고   :
    - 점만 검사하는 격자에서는 두께 1짜리 장애물을 그대로 뚫고 지나가 버리는데, 좌표 2배 확대로 해결
    - 내부 판정을 4방향으로만 하면 오목 꼭짓점 p4가 내부로 잘못 막히므로 8방향 검사가 필요
    - L자 장애물 영역을 격자에 초기화하는 부분이 생각보다 까다로웠음
"""

from collections import deque

# 좌표 1~100 -> 2배 확대 시 2~200, 양옆 여유 포함
SIZE = 203
DX = [-1, 1, 0, 0]
DY = [0, 0, -1, 1]
INF = int(1e9)


class Obstacle:
    """
    L자 장애물. 네 점 p1~p4 중 p4가 오목한 꼭짓점이다.
    L자 영역 = (p1, p4) / (p2, p4) / (p3, p4)를 대각으로 하는 직사각형 3개의 합집합.
    """

    def __init__(self, idx, points):
        self.idx = idx
        self.p1 = (points[0], points[1])
        self.p2 = (points[2], points[3])
        self.p3 = (points[4], points[5])
        self.p4 = (points[6], points[7])

    @staticmethod
    def _fill_rect(grid, a, b, value):
        """a, b를 대각 꼭짓점으로 하는 직사각형(경계 포함)을 value로 채운다."""
        for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                grid[x][y] = value

    def imprint(self, grid):
        """grid에 이 장애물이 차지하는 영역(경계 포함)을 자기 번호로 표시한다."""
        for corner in (self.p1, self.p2, self.p3):
            self._fill_rect(grid, corner, self.p4, self.idx)


def build_blocked(grid):
    """장애물의 엄밀한 내부(= 8방향 이웃이 모두 같은 장애물인 점)만 True로 표시한다."""
    blocked = [[False] * SIZE for _ in range(SIZE)]
    for x in range(1, SIZE - 1):
        for y in range(1, SIZE - 1):
            owner = grid[x][y]
            if owner == 0:          # 빈 공간
                continue
            if all(grid[x + a][y + b] == owner
                   for a in (-1, 0, 1) for b in (-1, 0, 1)):
                blocked[x][y] = True
    return blocked


def min_turns(blocked, start, goal):
    """0-1 BFS로 start -> goal 최소 꺾임 횟수를 구한다."""
    sx, sy = start
    gx, gy = goal

    # dist[x][y][d] = (x, y)에 방향 d로 도착했을 때의 최소 꺾임 횟수
    dist = [[[INF] * 4 for _ in range(SIZE)] for _ in range(SIZE)]
    dq = deque()

    # 첫 이동 방향은 자유이므로 4방향 모두 비용 0에서 시작
    for d in range(4):
        dist[sx][sy][d] = 0
        dq.append((0, sx, sy, d))

    while dq:
        cost, x, y, d = dq.popleft()
        if cost > dist[x][y][d]:    # 이미 더 좋은 값으로 처리된 상태
            continue

        for nd in range(4):
            nx, ny = x + DX[nd], y + DY[nd]
            if not (0 <= nx < SIZE and 0 <= ny < SIZE) or blocked[nx][ny]:
                continue

            ncost = cost + (d != nd)    # 방향이 바뀌면 꺾임 +1
            if ncost < dist[nx][ny][nd]:
                dist[nx][ny][nd] = ncost
                # 비용 0인 간선은 앞에, 비용 1인 간선은 뒤에 넣는다
                if d == nd:
                    dq.appendleft((ncost, nx, ny, nd))
                else:
                    dq.append((ncost, nx, ny, nd))

    return min(dist[gx][gy])


if __name__ == '__main__':
    # 모든 좌표를 2배로 확대해서 읽는다
    start = tuple(int(v) * 2 for v in input().split())
    goal = tuple(int(v) * 2 for v in input().split())

    # 0: 빈 공간, k: k번 장애물(경계 포함)
    grid = [[0] * SIZE for _ in range(SIZE)]
    n = int(input())
    for idx in range(1, n + 1):
        points = [int(v) * 2 for v in input().split()]
        Obstacle(idx, points).imprint(grid)

    blocked = build_blocked(grid)
    print(min_turns(blocked, start, goal))
