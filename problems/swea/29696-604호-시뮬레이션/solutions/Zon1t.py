"""
[SW Expert Academy 29696] 604호 시뮬레이션
https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD5x0z6c-DHBISc&categoryId=AaD5x0z6c-DHBISc&categoryType=CODE

작성자 : @Zon1t
결과   : 통과
"""


from collections import deque
 
# TODO 0. 기초공사
DEBUG = False
 
INF = int(1e9)
dxdy = [(0,1),(1,0),(0,-1),(-1,0)] # 우, 하, 좌, 상 (우선순위 순서)
inrange = lambda x, y : bool(0<=x<N and 0<=y<N)
 
def myprint(string, in_ma):
    if not DEBUG:
        return
    print(f"================{string}===================")
    for row in in_ma:
        for val in row:
            print(f"{val:2d}", end = " ")
        print()
 
# TODO 1. 함수들
 
def snake_order():
    # ㄹ자 순서대로 (x,y) 좌표를 돌려줌
    order = []
    for x in range(N):
        if x % 2 == 0:
            for y in range(N):
                order.append((x,y))
        else:
            for y in range(N-1, -1, -1):
                order.append((x,y))
    return order
 
def bfs():
    # 1차 팀 편성 : 인접 + 실력 차이 D 이하면 같은 팀
    global visited, group_sum, group_cnt, alone_list
    q = deque()
    visited = [[0]*N for _ in range(N)]
 
    g_num = 0
    group_sum = [0] # 팀 번호는 1부터 쓸거라 0번은 비워둠
    group_cnt = [0]
    alone_list = []
 
    for x in range(N):
        for y in range(N):
            if visited[x][y]:
                continue
            if not matrix[x][y]: # 빈자리
                continue
            # bfs 시작
            g_num += 1
            q.append((x,y))
            visited[x][y] = g_num
            group_sum.append(0)
            group_cnt.append(0)
 
            while q:
                cur_x, cur_y = q.popleft()
                group_sum[g_num] += abil_ma[cur_x][cur_y]
                group_cnt[g_num] += 1
 
                for dx, dy in dxdy:
                    nx, ny = cur_x+dx, cur_y+dy
                    if not inrange(nx,ny):
                        continue
                    if not matrix[nx][ny]: # 빈자리
                        continue
                    if visited[nx][ny]:
                        continue
                    # 지금 보고 있는 사람(cur)이랑 옆사람(n)의 차이
                    if abs(abil_ma[cur_x][cur_y] - abil_ma[nx][ny]) <= D:
                        visited[nx][ny] = g_num
                        q.append((nx,ny))
 
            if group_cnt[g_num] == 1:
                alone_list.append((matrix[x][y], x, y))
 
    alone_list.sort() # 직원 ID 작은 순서
    myprint("aft 1st grouping", visited)
 
def merge_alone():
    # 혼자인 직원을 인접한 팀에 병합
    for num, x, y in alone_list:
        my_group = visited[x][y]
        if group_cnt[my_group] != 1: # 앞 사람이 나한테 합쳐졌으면 이미 혼자가 아님
            continue
 
        candidate = (INF, INF) # (평균과의 차이, 방향 번호)
        for ith, (dx, dy) in enumerate(dxdy):
            nx, ny = x+dx, y+dy
            if not inrange(nx,ny):
                continue
            if not matrix[nx][ny]:
                continue
            that_group = visited[nx][ny]
            aver = group_sum[that_group] // group_cnt[that_group]
            diff = abs(aver - abil_ma[x][y])
 
            temp = (diff, ith)
            candidate = min(candidate, temp)
 
        if candidate == (INF, INF): # 주변에 아무도 없음 -> 그냥 혼자
            continue
 
        _, final_ith = candidate
        dx, dy = dxdy[final_ith]
        that_group = visited[x+dx][y+dy]
 
        visited[x][y] = that_group # 팀에 들어감 (평균은 바로 갱신)
        group_sum[that_group] += abil_ma[x][y]
        group_cnt[that_group] += 1
 
    myprint("aft merge", visited)
 
def grow():
    # 팀 평균 이상이면 +1, 아니면 +2
    for x in range(N):
        for y in range(N):
            if not matrix[x][y]:
                continue
            num = visited[x][y]
            group_abil = group_sum[num] // group_cnt[num]
            if abil_ma[x][y] >= group_abil:
                abil_ma[x][y] += 1
            else:
                abil_ma[x][y] += 2
 
def morning(day):
    today_Lv = levels[day]
 
    for x in range(N):
        for y in range(N): # 아침에는 모두 있음
            if abil_ma[x][y] >= today_Lv:
                abil_ma[x][y] += 1
            else:
                mental_ma[x][y] -= min(4, today_Lv - abil_ma[x][y])
                if mental_ma[x][y] <= 0:
                    num = matrix[x][y]
                    for_store[num] = abil_ma[x][y] # 나간 직원의 실력 저장
                    matrix[x][y] = 0 # 비워줌
 
def lunch():
    for x in range(N):
        for y in range(N):
            if matrix[x][y]:
                mental_ma[x][y] += 2
    bfs()
    merge_alone()
    grow()
 
def dinner():
    order = snake_order()
 
    # 1. 남은 직원을 ㄹ자 순서대로 모음
    people = [] # (직원 ID, 실력, 정신력)
    for x, y in order:
        if matrix[x][y]:
            people.append((matrix[x][y], abil_ma[x][y], mental_ma[x][y]))
 
    # 2. 나갔던 직원은 ID 작은 순서대로 뒤에 붙임 (정신력 10)
    for num in range(1, N**2 + 1):
        if for_store[num]:
            people.append((num, for_store[num], 10))
            for_store[num] = 0
 
    # 3. 앞자리부터 다시 앉힘
    for idx, (x, y) in enumerate(order):
        matrix[x][y], abil_ma[x][y], mental_ma[x][y] = people[idx]
 
 
T = int(input())
 
 
for testcase in range(1, T+1):
    N, Days, D = map(int, input().split())
 
 
    abil_ma, mental_ma = [], []
    for _ in range(N):
        abil_ma.append(list(map(int, input().split())))
 
    for _ in range(N):
        mental_ma.append(list(map(int, input().split())))
 
    levels = list(map(int, input().split()))
    assert len(levels) == Days, "insufficient problems"
 
    cur = 1
    reverse = 0
 
    matrix = []
    for x in range(N):
        matrix.append([])
 
        for y in range(N):
            if reverse:
                matrix[-1].insert(0, cur)
            else:
                matrix[-1].append(cur)
            cur += 1
        reverse ^= 1
 
    myprint("initial abil", abil_ma)
    myprint("initial mental", mental_ma)
    myprint("initial", matrix)
    for_store = [0 for _ in range(N**2 + 1)] # 나간 직원용
 
    print(f"#{testcase}")
    for day in range(Days): # index 위해서 0부터
 
        morning(day)
        myprint(f"day {day+1} aft morning, abil", abil_ma)
 
        lunch()
        myprint(f"day {day+1} aft lunch, abil", abil_ma)
 
        dinner()
        myprint(f"day {day+1} aft dinner, matrix", matrix)
 
        print(sum(map(sum, abil_ma)), sum(map(sum, mental_ma)))