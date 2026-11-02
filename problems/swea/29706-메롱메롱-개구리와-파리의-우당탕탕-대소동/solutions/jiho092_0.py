"""
[SW Expert Academy 29706] 메롱메롱 개구리와 파리의 우당탕탕 대소동
https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD6W7R6kFPHBIPk&categoryId=AaD6W7R6kFPHBIPk&categoryType=CODE

작성자 : @jiho092
결과   : 통과
"""


"""
문제 : 메롱 개구리와 파리
목적 : 개구리들이 K턴 동안 잡아먹은 파리의 총 마리수 구하기
조건 :
    1. 개구리가 허겁지겁 열매를 주워 먹어서 능력이 생김
    2. 연못은 N x N 격자로 이루어짐, 각 칸은 0(물), 1(연잎)으로 이루어짐
    3. 연못에는 T마리의 개구리와 F마리의 파리가 살고 있음
    4. 개구리 정보
        1. 하나의 연잎 위에는 최대 한 마리의 개구리만 있을 수 있음.
        2. 초기 입력으로 주어지는 첫 번째 개구리 단 1마리만 깨어 있으며,
        3. 나머지 개구리들은 깊은 잠에 빠져있음
        4. 깊은 잠은 다른 개구리의 침 범벅으로만 깨울 수 있습니다.
    5. 파리 정보 :
        1. 물 위나 연잎 위를 자유롭게 날아다님
        2. 여러 마리의 파리가 같은 칸에 겹쳐있을 수 있음
    6. 1초마다 다음과 같은 과정이 순서대로 일어남
        - 충돌을 방지하기 위해 개구리들의 행동은 번호가 작은 개구리부터 순서대로 개별 진행

        [1]. 개구리의 메롱과 침 범벅 동료 깨우기
        1. 현재 깨어있는 (수면 / 식곤증 상태가 아닌) 개구리는 제자리에서 혀의 길이 L만큼
            혀를 강하게 휘두릅니다.
        (1). 메롱 :
            1. 개구리의 현재 위치에서 L칸 안에 존재하는 모든 파리를 단숨에 잡아먹음
            2. 혀는 공중으로 내두르기 때문에 해당 범위에 있는 다른 개구리에게는 아무 영향을 주지 않음
        (2). 침 범벅:
            1. 개구리가 혀를 휘두를 때 튀는 침 떄문에, 정확히 L+1인 칸에 있던 '깊은 잠에 빠진'
                동료 개구리들이 화들짝 놀라 즉시 잠에서 깸
                이 턴에 깨어난 개구리는 다음 턴부터 파리 먹기가 가능
                (식곤증이 온 동료 개구리는 깨우지 않음)

        [2]. 원심력에 의한 연잎 침수 및 대피
        1. 개구리가 혀를 휘둘러 파리를 1마리 이상 잡아먹은 경우 다음 과정이 진행
            [2-1] 연잎 침수 :
                1. 혀를 강하게 휘두른 원심력 때문에, 개구리가 현재 밟고 있던
                연잎은 즉시 가라앉아 물(0)로 변하게 됨
            [2-2] 가장 가까운 연잎으로 대피 :
                1. 개구리는 가라앉는 연잎을 피해 살아남기 위해,
                    현재 위치에서 맨해튼 거리가 가장 가까운 빈 연잎으로 점프하여 대피합니다.
                2. 공중으로 도약하므로 중간에 물이 있더라도 거리에 상관없이 뛰어넘을 수 있음
                3. 대피하려는 연잎에 다른 개구리가 이미 존재한다면 그곳으로는 점프 불가
                    (즉, 현재 맵에 존재하는 개구리가 없는 빈 연잎들 중 가장 가까운 곳을 찾음)
                4. 최단 거리에 있는 빈 연잎이 여러 개라면, 행 번호 작은순 열 번호 작은 순
            [2-3] 익사 :
                1. 만약 대피할 연잎이 아예 없다면, 개구리는 물에 빠져 죽습니다.
                    (게임에서 영구 제외)
                2. 원피스 세계관에서 악마의 열매 능력자는 바다의 미움을 샀기 때문에
                    헤엄칠 수 없는 맥주병이기 때문
            [2-4] 식곤증 :
                1. 무사히 빈 연잎으로 대피를 마친 개구리는 배가 불러 새로 도착한 연잎
                    위에서 즉시 자신의 '개구리 번호'만큼의 턴 동안 식곤증에 빠집니다.
        2. 파리를 1마리도 못 잡았다면, 아래 과정을 생략하고 제자리에 가만히 있습니다.

        [3]. 파리의 이동 :
            1. 살아남은 파리들은 자신이 바라보는 방향으로 각각 1칸씩 동시에 비행합니다.
            2. 만약 이동하려는 칸이 격자 범위를 벗어난다면, 방향을 정반대로 바꾸고 바뀐 방향으로
                한칸 이동합니다.

        [4]. 수면 카운트 감소 :
            1. 식곤증에 빠져 잠들어 있는 개구리들의 수면 턴 수가 1 감소합니다.
            2. 수면 턴이 0이 되면 다음 턴부터 다시 포식을 시도할 수 있습니다.
아이디어 :
    1. 전체 흐름 : 개구리의 메롱과 침범벅 - 원심력에 의한 연잎 침수 및 대피
                    - 파리의 이동 - 수면 카운트 감소
"""


from collections import deque

dirs = [(-1,0),(1,0),(0,-1),(0,1)]  # 위아왼오

def in_range(i, j):
    return 0 <= i < N and 0 <= j < N

def custom_print(string, arr):
    print(f'========{string}=========')
    for row in arr:
        print(row)
    print('==========================')

####################
# 0. 함수 생성
####################

# [1]. 메롱
def merong(frog_num):
    # (1). 개구리 정보 불러오기
    fi, fj, fl = frog_info[frog_num]

    que = deque([(fi, fj)])
    visit = [[0]*N for _ in range(N)]
    visit[fi][fj] = 1

    cl, cnt = 0, 0

    while que:
        for _ in range(len(que)):
            ci, cj = que.popleft()

            # (2). L이하면 파리 잡아먹기
            if cl <= fl and fly_arr[ci][cj]:
                for fnum in fly_arr[ci][cj]:
                    alive_fly.remove(fnum)
                    cnt += 1
                fly_arr[ci][cj].clear()

            # (3). L+1이면 잠든 개구리 깨우기
            elif cl == fl + 1:
                if frog_arr[ci][cj] != 0:  # noqa: SIM102
                    # (3-1). 살아 있고, 깊은 잠을 자고 있는 개구리
                    if frog_arr[ci][cj] in alive_frog and frog_sleep[frog_arr[ci][cj]] == -1:
                        frog_sleep[frog_arr[ci][cj]] = 0
                        awake_frog.add(frog_arr[ci][cj])

            # (4). 다음 탐색
            for di, dj in dirs:
                ni = ci + di
                nj = cj + dj
                if in_range(ni, nj) and visit[ni][nj] == 0:
                    visit[ni][nj] = 1
                    que.append((ni, nj))

        cl += 1

        # 혀 범위 이상이라면 종료
        if cl > fl + 1:
            break

    return cnt

# [2]. 이동할 연잎 찾기
def find_leaf(frog_num):
    # (1). 개구리 정보 불러오기
    fi, fj, _fl = frog_info[frog_num]

    # (2). 데이터 입력
    que = deque([(fi, fj)])
    visit = [[0] * N for _ in range(N)]
    visit[fi][fj] = 1
    status = False
    min_one = (N, N)

    while que:
        for _ in range(len(que)):
            ci, cj = que.popleft()

            # (1). 비어 있는 연잎이면 이동 가능
            if arr[ci][cj] == 1 and frog_arr[ci][cj] == 0:
                status = True
                min_one = min(min_one, (ci, cj))

            # (2). 탐색
            for di, dj in dirs:
                ni = ci + di
                nj = cj + dj

                if in_range(ni, nj) and visit[ni][nj] == 0:
                    visit[ni][nj] = 1
                    que.append((ni, nj))

        # (3). 현재 que에서 연잎을 찾았다면
        if status:
            return min_one

    # (4). 이동할 연잎이 없는 경우
    return None

# [3]. 개구리 이동
def frog_move(frog_num):
    fi, fj, _fl = frog_info[frog_num]

    # (1). 현재 연잎 제거
    arr[fi][fj] = 0
    frog_arr[fi][fj] = 0

    # (2). 이동할 연잎 찾기
    goal = find_leaf(frog_num)

    # (3). 이동할 연잎이 없다면 익사
    if goal is None:
        alive_frog.remove(frog_num)
        return

    # (4). 아니라면 개구리 정보 업데이트
    ni, nj = goal

    # 개구리 위치 변경
    frog_info[frog_num][0] = ni
    frog_info[frog_num][1] = nj

    frog_arr[ni][nj] = frog_num

    # 자신의 번호만큼 식곤증
    frog_sleep[frog_num] = frog_num

# [4]. 파리 이동
def fly_move():
    new_fly_arr = [[[] for _ in range(N)] for _ in range(N)]

    for fly_num in alive_fly:

        fi, fj, fd = fly_info[fly_num]

        di, dj = dirs[fd]

        ni = fi + di
        nj = fj + dj

        # 밖으로 나가면 방향 반전 후 이동
        if not in_range(ni, nj):
            fd ^= 1

            di, dj = dirs[fd]

            ni = fi + di
            nj = fj + dj

        fly_info[fly_num] = [ni, nj, fd]

        new_fly_arr[ni][nj].append(fly_num)

    return new_fly_arr

# [5]. 식곤증 감소
def sleep_down():
    for frog_num in alive_frog:
        if frog_sleep[frog_num] > 0:
            frog_sleep[frog_num] -= 1

####################
# 1. 입력 받기
####################
N, T, F, K = map(int, input().split())  # 격자 크기, 개구리 수, 파리 수, 턴 수

arr = [list(map(int, input().split())) for _ in range(N)]   # 0 : 물, 1 : 연잎

# 1.1 개구리 정보 받기
frog_info = [None] * (T+1)              # 개구리 행, 열, 혀 길이
frog_sleep = [-1] * (T+1)               # 개구리 수면 정보 (-1 : 깊은 잠, 0 : 깨어 있음, 1~ : 식곤증)
frog_arr = [[0]*N for _ in range(N)]    # 개구리 배열
alive_frog = set()                      # 살아있는 개구리 관리

for t in range(T):
    frog_num, fi, fj, fl = map(int, input().split())
    fi, fj = fi -1, fj - 1

    frog_info[frog_num] = [fi, fj, fl]
    frog_arr[fi][fj] = frog_num
    alive_frog.add(frog_num)

    # (1). 첫 번째 개구리 깨우기
    if t == 0:
        frog_sleep[frog_num] = 0

# 1.2 파리 정보 받기
fly_info = [None] * (F+1)               # 파리 행, 열, 방향
fly_arr = [[[] for _ in range(N)] for _ in range(N)]    # 파리 위치 3차원 배열
alive_fly = set()                       # 살아있는 파리 관리

for f in range(1, F+1):
    fi, fj, fd = (int(x)-1 for x in input().split())

    fly_info[f] = [fi, fj, fd]
    fly_arr[fi][fj].append(f)
    alive_fly.add(f)

####################
# 2. 게임 시작
####################
eat = 0

for turn in range(K):
    # 이번 턴에 깨어난 개구리 관리
    awake_frog = set()

    # [1]. 메롱
    for frog_num in range(1, T+1):
        # (1). 죽은 개구리 넘어가기
        if frog_num not in alive_frog:
            continue

        # (2). 깊은 잠
        if frog_sleep[frog_num] == -1:
            continue

        # (3). 식곤증
        if frog_sleep[frog_num] > 0:
            continue

        # (4). 이번 턴에 깨어난 개구리는 다음 턴부터 가능
        if frog_num in awake_frog:
            continue

        # (5). 파리 먹기
        cnt = merong(frog_num)

        # [2]. 개구리 대피 시키기
        if cnt:
            eat += cnt
            frog_move(frog_num)

    # [3]. 파리 이동
    fly_arr = fly_move()

    # [4]. 식곤증 감소
    sleep_down()

print(eat)
