"""
[SW Expert Academy 29672] 점령전
https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD28FJqwqXHBIPk&categoryId=AaD28FJqwqXHBIPk&categoryType=CODE

작성자 : @Hoesu
결과   : 통과 (실행 시간 74ms, 메모리 54,528KB)
접근   :
    - 클래스 쓰면 편하다.
회고   :
    - 구현 자체는 쉽지만, 디테일을 까먹지 않도록 조심해야 한다.
"""


from collections import deque


class Tower:
    def __init__(self, ti, tr, tc):
        self.r = tr
        self.c = tc
        self.idx = ti
        self.team = None

    def imprint(self):
        t_occupation[self.r][self.c] = self.idx

    def activate(self, team_id):
        self.team = team_id

    def attack(self):
        if self.team is None:
            return None

        targets = []
        for k, v in players.items():
            if v.in_tower:
                continue
            if v.team == self.team:
                continue
            dist = abs(self.r-v.r) + abs(self.c-v.c)
            targets.append([dist, v.power, k])

        if not targets:
            return None

        targets.sort(key=lambda x: [x[0], x[1]])
        _, _, target_id = targets[0]
        scores[self.team-1] += 10
        return target_id


class Player:
    def __init__(self, pi, pt, pr, pc, ps, pw):
        self.r = pr
        self.c = pc
        self.idx = pi
        self.team = pt
        self.speed = ps
        self.power = pw
        self.in_tower = False

    def imprint(self):
        p_occupation[self.r][self.c].add(self.idx)

    def unprint(self):
        p_occupation[self.r][self.c].discard(self.idx)

    def move(self):
        if self.in_tower:
            return
        if t_occupation[self.r][self.c] > 0:
            return

        self.unprint()
        que = deque()
        que.append((self.r, self.c))
        vst = [[0] * N for _ in range(N)]
        vst[self.r][self.c] = 1
        path = {}
        tr, tc = None, None

        while que:
            cr, cc = que.popleft()
            if t_occupation[cr][cc] > 0:
                tr, tc = cr, cc
                break

            for d in range(4):
                nr, nc = cr + DR[d], cc + DC[d]
                if not(0 <= nr < N and 0 <= nc < N):
                    continue
                if vst[nr][nc] != 0:
                    continue
                if geography[nr][nc] != 0:
                    continue

                path[(nr, nc)] = (cr, cc)
                que.append((nr, nc))
                vst[nr][nc] = 1

        if tr is None and tc is None:
            self.imprint()
            return

        nr, nc = tr, tc
        route = [(nr, nc)]
        while True:
            cr, cc = path[(nr, nc)]
            if cr == self.r and cc == self.c:
                break
            nr, nc = cr, cc
            route.append((nr, nc))

        route.reverse()
        if len(route) >= self.speed:
            self.r, self.c = route[self.speed - 1]
        else:
            self.r, self.c = route[-1]
        self.imprint()
        if self.r == tr and self.c == tc:
            self.in_tower = True


if __name__ == '__main__':
    TEST_CASE = int(input())
    for TC in range(1, TEST_CASE+1):
        print(f'#{TC}', end=' ')

        DR = [-1, 1, 0, 0]
        DC = [0, 0, -1, 1]

        N, M, K, P, L = map(int, input().split())
        geography = [list(map(int, input().split())) for _ in range(N)]
        p_occupation = [[set() for _ in range(N)] for _ in range(N)]
        t_occupation = [[0] * N for _ in range(N)]
        scores = [0] * K

        towers = {}
        for i in range(1, M+1):
            r, c = map(int, input().split())
            towers[i] = Tower(i, r, c)
            towers[i].imprint()

        players = {}
        for i in range(1, P+1):
            t, r, c, s, w = map(int, input().split())
            players[i] = Player(i, t, r, c, s, w)
            players[i].imprint()

        time = 1
        for _ in range(L):

            # TODO 0: 조기 종료 조건
            if not any(not player.in_tower for player in players.values()):
                break

            # TODO 1: 플레이어 이동
            for key in players:  # noqa: PLC0206
                players[key].move()

            # TODO 2: 포탑 점령
            for key in towers:  # noqa: PLC0206
                r, c = towers[key].r, towers[key].c
                if len(p_occupation[r][c]) == 0:
                    continue

                candidates = list(p_occupation[r][c])

                if len(candidates) == 1:
                    survivor_id = candidates[0]
                else:
                    candidates.sort(key=lambda x: -players[x].power)
                    survivor_id = candidates[0]

                survivor_team = players[survivor_id].team
                scores[survivor_team - 1] += len(candidates) - 1
                towers[key].activate(survivor_team)
                players[survivor_id].in_tower = True

                for killed_id in candidates:
                    if killed_id == survivor_id:
                        continue
                    players[killed_id].unprint()
                    players.pop(killed_id)

            # TODO 3: 포탑 공격
            dead_players = set()
            for key in towers:  # noqa: PLC0206
                killed_player = towers[key].attack()
                if killed_player is not None:
                    dead_players.add(killed_player)

            for key in dead_players:
                players[key].unprint()
                players.pop(key)

            # TODO 4: 시간 증가
            time += 1

        # TODO 5: 타워 최종 점유 팀 30점씩 추가
        for tower in towers.values():
            if tower.team is not None:
                scores[tower.team - 1] += 30

        # 정답 출력
        print(*scores)
