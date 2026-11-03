"""
[SW Expert Academy 2383] 점심 식사 시간
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5-BEE6AK0DFAVl

작성자 : @Hyunnniiii
결과   : 통과 (실행 시간 282ms, 메모리 64,728KB)
복잡도 : (선택) 시간 O( ), 공간 O( )
접근   :
    - 각 사람마다 어느 계단을 이용할지는 백트래킹으로 모든 경우를 구했음
    - 각 계단마다 도착 시간 순으로 정렬한 뒤, 시간 1씩 늘려가면서 사람들을 계단에 투입했음
회고   :
    - 생각보다 계단 3명 제한 조건 처리하는게 까다로웠음. 풀어보면 도움 될 것 같음!!
"""


def btrk(idx):
    global ans

    if idx == len(people):
        # 각자 걸리는 시간 구하기
        arrive_time = get_time()

        # 계단 투입
        ans = min(ans, simulation(arrive_time))
        return

    # 1번 계단 선택
    selected[idx] = 0
    btrk(idx+1)

    # 2번 계단 선택
    selected[idx] = 1
    btrk(idx+1)


def get_time():
    arrive_time = [[], []]

    for i in range(len(people)):
        r, c = people[i]
        stair_idx = selected[i]
        sr, sc, length = stairs[stair_idx]

        dist = abs(r-sr) + abs(c-sc)

        # 투입 시간 기록
        arrive_time[stair_idx].append(dist+1)

    arrive_time[0].sort()
    arrive_time[1].sort()

    return arrive_time


def simulation(arrive_time):
    nxt = [0, 0]    # 각 계단에서 다음에 투입할 사람 인덱스
    end_time = [[], []]   # 각 사람마다 계단 다 내려간 시간
    time = 0

    # 모든 사람이 계단에 투입될 때까지
    while nxt[0] < len(arrive_time[0]) or\
        nxt[1] < len(arrive_time[1]):

        # 각 계단에 대해 계산
        for s in range(2):
            stair_length = stairs[s][2]

            while nxt[s] < len(arrive_time[s]):
                cnt = nxt[s]

                # 아직 투입 시간 아니면
                if arrive_time[s][cnt] > time:
                    break

                # 이미 3명 이용 중 > 맨 앞 사람 확인
                if cnt >= 3 and end_time[s][cnt-3] > time:
                    break

                # 새로운 사람 투입
                end_time[s].append(time + stair_length)
                nxt[s] += 1

        time += 1

    return max(end_time[0] + end_time[1])


###############################################
TC = int(input().strip())
for test_case in range(1, TC+1):
    N = int(input().strip())
    arr = [list(map(int, input().split())) for _ in range(N)]

    people = []     # 각 사람들의 좌표
    stairs = []     # 계단 좌표, 계단 길이

    for r in range(N):
        for c in range(N):
            if arr[r][c] == 1:
                people.append((r, c))
            elif arr[r][c] >= 2:
                stairs.append((r, c, arr[r][c]))

    ans = float('inf')
    selected = [0] * len(people)    # 각 사람마다 이용할 계단 번호 표시
    btrk(0)

    print(f'#{test_case}', ans)
