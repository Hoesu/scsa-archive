"""
[SW Expert Academy 29706] 메롱메롱 개구리와 파리의 우당탕탕 대소동
https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD6W7R6kFPHBIPk&categoryId=AaD6W7R6kFPHBIPk&categoryType=CODE

작성자 : @jiho092
결과   : 통과
"""


from collections import deque

didj = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def NNBB(si, sj, L):

    q = deque()
    q.append([si, sj])

    visited = [[0] * N for _ in range (N)]
    visited[si][sj] = 1

    tmp_L = 0
    ate_fly_cnt = 0

    while q:

        for _ in range (len(q)):
            ci, cj = q.popleft()

            #파리먹기
            if tmp_L <= L:
                if sum(fly_arr[ci][cj]) > 0:
                    ate_fly_cnt += sum(fly_arr[ci][cj])
                    fly_arr[ci][cj] = [0] * 4

            #동료 깨우기
            if tmp_L == L+1:
                if toad_arr[ci][cj] != 0:
                    waked_toad_lst.add(toad_arr[ci][cj])

            for di, dj in didj:
                ni = ci + di
                nj = cj + dj

                if 0 <= ni < N and 0 <= nj < N and visited[ni][nj] == 0:
                    visited[ni][nj] = 1
                    q.append([ni, nj])
        tmp_L += 1

        if tmp_L > L+1:
            break

    return ate_fly_cnt


def manhattan(r1, c1, r2, c2):
    return abs(r1 - r2) + abs(c1 - c2)


N, T, F, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range (N)]
toad_info = dict()
fly_arr = [[[0] * 4 for _ in range (N)] for _ in range (N)]
toad_arr = [[0] * N for _ in range (N)]


#첫 번째 입력 개구리
#r, c, L, 상태 순으로 저장되는 딕셔너리
num, r, c, l = map(int, input().split())
toad_info[num] = [r-1, c-1, l, 0]
toad_arr[r-1][c-1] = num

for _ in range (T-1):
    num, r, c, l = map(int, input().split())
    toad_info[num] = [r-1, c-1, l, -1]
    toad_arr[r - 1][c - 1] = num

for _ in range (F):
    r, c, d = map(lambda x: int(x)-1, input().split())
    fly_arr[r][c][d] += 1

ans = 0

for k in range (1, K+1):

    #이번 턴에서 깨움 당하는 애들 저장
    waked_toad_lst = set()

    for toad_num in list(toad_info.keys()):

        tr, tc, tl, status = toad_info[toad_num]
        #깨어있는 상태가 아니면 넘어간다.
        if status != 0:
            continue

        #[1]개구리의 메롱과 침 범벅 동료 깨우기
        res =  NNBB(tr, tc, tl)

        if res == 0:
            continue

        #답 더해주기
        ans += res

        #[2] 원심력에 의한 연잎 침수 및 대피
        arr[tr][tc] = 0 #물이 된다.
        toad_arr[tr][tc] = 0 #개구리 arr에서도 빠진다.

        leaf_hubo = []

        for i in range (N):
            for j in range (N):
                if arr[i][j] == 0 or toad_arr[i][j] != 0: #물이면 넘어가고 다른 개구리 있으면 넘어가고..
                    continue
                tmp_d = manhattan(tr, tc, i, j)
                leaf_hubo.append([tmp_d, i, j])


        #갈 곳이 없다. 죽어야 함.
        if not leaf_hubo:
            toad_info.pop(toad_num)
            continue

        #갈 곳 있음.
        leaf_hubo = sorted(leaf_hubo, key=lambda x: (x[0], x[1], x[2]))
        toad_info[toad_num][0], toad_info[toad_num][1] = leaf_hubo[0][1], leaf_hubo[0][2]
        toad_arr[leaf_hubo[0][1]][leaf_hubo[0][2]] = toad_num

        #식곤증에 빠지기.
        toad_info[toad_num][3] = toad_num


    #동료 상태 0으로 바꾸기

    for nakama in waked_toad_lst:
        if toad_info.get(nakama):
            if toad_info[nakama][3] == -1:
                toad_info[nakama][3] = 0

    new_fly_arr = [[[0] * 4 for _ in range (N)] for _ in range (N)]
    #[3] 파리 이동
    for i in range (N):
        for j in range (N):
            for d in range (4):
                nd = d
                ni = i + didj[nd][0]
                nj = j + didj[nd][1]

                if not (0 <= ni < N and 0 <= nj < N):
                    nd ^= 1
                    ni = i + didj[nd][0]
                    nj = j + didj[nd][1]

                new_fly_arr[ni][nj][nd] += fly_arr[i][j][d]

    fly_arr = new_fly_arr

    #[4] 수면 카운트 감소
    for toad_num in list(toad_info.keys()):
        tr, tc, tl, status = toad_info[toad_num]
        if status > 0:
            toad_info[toad_num][3] -= 1

print(ans)