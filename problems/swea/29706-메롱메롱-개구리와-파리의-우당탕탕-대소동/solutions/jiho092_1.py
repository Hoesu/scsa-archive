"""
[SW Expert Academy 29706] 메롱메롱 개구리와 파리의 우당탕탕 대소동
https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD6W7R6kFPHBIPk&categoryId=AaD6W7R6kFPHBIPk&categoryType=CODE

작성자 : @jiho092
결과   : 통과
"""


# N * N, T 개구리, F 파리, K턴
# 2 <= N <= 20, 1 <= T <= 10, 1 <= F <= 20, 1 <= K  <= 1000

from collections import deque

dij = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def custom_print(msg=None, mode=False):
    if not mode:
        return

    if msg:
        print(msg)
    print(frog_info)
    print('깊은 잠: ', sleep)
    print('죽음   :', dead)
    for i in range(N):
        print(*board[i], end='\t')
        print(*fly[i], end='\t')
        print(*frog[i])
    print('---')


def try_eat(num):
    global ans

    si, sj, L, _ = frog_info[num]

    q = deque()
    q.append((si, sj))

    visited = [[-1] * N for _ in range(N)]
    visited[si][sj] = 0

    now_l = 0
    eated = 0
    while q:
        now_l += 1

        for _ in range(len(q)):
            ci, cj = q.popleft()

            if visited[ci][cj] <= L and fly[ci][cj]:
                ans += len(fly[ci][cj])
                eated = 1
                fly[ci][cj] = []

            if visited[ci][cj] == L+1:
                if frog[ci][cj] in sleep:
                    nxt_awake.add(frog[ci][cj])
                    sleep.discard(frog[ci][cj])
                continue

            for di, dj in dij:
                ni, nj = ci + di, cj + dj
                # 범위 내, 미방문(-1)
                if 0 <= ni < N and 0 <= nj < N and visited[ni][nj] == -1:
                    visited[ni][nj] = visited[ci][cj] + 1
                    q.append((ni, nj))

        if now_l > L+1:
            break

    return eated


def jump(num):
    si, sj, *_ = frog_info[num]

    frog[si][sj] = 0
    board[si][sj] = 0

    min_one = (1000, N, N)

    for i in range(N):
        for j in range(N):
            if board[i][j] == 1 and frog[i][j] == 0:
                dist = abs(si-i) + abs(sj-j)
                min_one = min(min_one, (dist, i, j))

    if min_one[0] != 1000:
        ni, nj = min_one[1], min_one[2]
        frog[ni][nj] = num
        frog_info[num][0], frog_info[num][1] = ni, nj
    else:
        dead.add(num)


def move(fly_pos):
    new_fly = [[[] for _ in range(N)] for _ in range(N)]
    new_fly_pos = set()
    for ci, cj in fly_pos:
        for cd in fly[ci][cj]:
            ni, nj = ci + dij[cd][0], cj + dij[cd][1]

            # 범위 밖, 방향 반대
            if not (0 <= ni < N and 0 <= nj < N):
                if cd % 2:
                    cd -= 1
                else:
                    cd += 1
                ni, nj = ci + dij[cd][0], cj + dij[cd][1]

            new_fly[ni][nj].append(cd)
            new_fly_pos.add((ni, nj))

    return new_fly, new_fly_pos


# [입력] N, T, F, K
N, T, F, K = map(int, input().strip().split())
board = [list(map(int, input().strip().split())) for _ in range(N)]
frog = [[0] * N for _ in range(N)]
frog_info = [[] for _ in range(T+1)]
sleep, dead = set(), set()
for idx in range(T):
    num, i, j, L = map(int, input().strip().split())
    i, j = i-1, j-1
    frog[i][j] = num

    if idx != 0:
        sleep.add(num)
        frog_info[num] = [i, j, L, 1001]
    else:
        frog_info[num] = [i, j, L, 0]

fly = [[[] for _ in range(N)] for _ in range(N)]
fly_pos = set()
for idx in range(F):
    i, j, d = (int(x)-1 for x in input().strip().split())
    fly[i][j].append(d)
    fly_pos.add((i, j))

# 정답 저장용.
ans = 0

# 디버그 모드
DEBUG_MODE = 0

custom_print('시작 전', DEBUG_MODE)
for cycle in range(1, K+1):
    # 1. 개구리
    nxt_awake = set()
    for num in range(1, T+1):
        if num not in sleep and num not in dead:
            if frog_info[num][3] > cycle:
                continue

            eated = try_eat(num)

            if eated:
                if DEBUG_MODE:
                    print(f'{cycle}턴, {num}번 개구리 섭취 완료')
                jump(num)
                frog_info[num][3] = cycle + num
                custom_print(f'{cycle}턴, {num}번 개구리 이동 완', DEBUG_MODE)

    for new in nxt_awake:
        frog_info[new][3] = cycle

    # 2. 파리
    fly, fly_pos = move(fly_pos)
    custom_print(f'{cycle}턴, 파리 이동 완료', DEBUG_MODE)

# [출력] 잡아먹은 파리 수
print(ans)
