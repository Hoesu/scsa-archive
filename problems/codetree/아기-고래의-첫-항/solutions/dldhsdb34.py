"""
[Codetree baby-whale-first-voyage] 아기 고래의 첫 항
https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/baby-whale-first-voyage/description

작성자 : @dldhsdb34
결과   : 통과 (실행 시간 119 ms, 메모리 12 MB)
복잡도 : (선택) 시간 O( ), 공간 O( )
접근   : 접근하기가 참!! 
  -
  -
회고   : 고래야 잘가 
  -
"""


from collections import deque
# 디버그 모드
debug_mode = 0
dirs = [[0,-1],[1,0],[0,1],[-1,0]] # 좌 하 우 상
table = [[0,1,3,2],[1,2,0,3],[2,3,1,0],[3,0,2,1]] # 현재 바라보는 방향-> 좌회전-> 우회전-> 180도 회전


# 커스텀 프린트
def custom_print(str,arr):
    if debug_mode == 1:
        print(str)
        for row in arr:
            print(*row)
        print()

def move_turtle():
    global tr,tc,td
    cr,cc,cd = tr,tc,td
    while True:
        cur_dir_table = table[cd]
        for direction in cur_dir_table:
            nr,nc = cr+dirs[direction][0], cc+dirs[direction][1]
            if 0<=nr<n and 0<=nc<n and already_go[nr][nc] == 0 and board[nr][nc] == 0:
                # 아직 방문하지 않은 바다칸 인지 확인
                # 결과 처리
                already_go[nr][nc] = 1
                result.append((nr+1,nc+1))
                cr,cc,cd = nr,nc,direction # 이동 위치, 방향 업데이트 -> 다시 while 문 돌기
                break
        else: # 인접한 칸에 방문 가능한 바다가 없으면 종료
            break # while 문 종료

    custom_print("거북이가 잘 가고 있나", already_go)
    return cr,cc,cd # 최종 위치, 방향 반환


def find_sea(sr,sc,already_go):
    visited = [[0] * n for _ in range(n)]
    visited[sr][sc] = 1 # sr,sc 에서 부터 아직 방문하지 않은 바다 중 가장 가까운 칸으로 갈 예정
    q = deque()
    q.append((sr,sc,0))
    hubo = []
    while q:
        for _ in range(len(q)):
            cr,cc,cur_dist= q.popleft()

            for h in range(4): # 최단거리 이동할 때, 좌,하,우,상 순으로 먼저 이동
                nr,nc = cr+dirs[h][0], cc+dirs[h][1]
                if 0<=nr<n and 0<=nc<n and visited[nr][nc] == 0 and board[nr][nc] == 0:
                    # 암초는 갈 수 없고, 이미 방문한 바다는 갈 수 있다.
                    visited[nr][nc] = 1
                    if already_go[nr][nc] == 0:
                        hubo.append((cur_dist+1,nr,nc,h)) # 아직 고래가 방문하지 않은 바다를 만났다면 hubo에 거리,nr,nc, 사실 마지막 방향만 알면 된다.
                    q.append((nr,nc,cur_dist+1))
        if hubo:
            # 아직 고래가 방문하지 않은 바다를 만났다면 거리가 짧고, 행이 작고, 열이 작은 칸 선택
            hubo.sort(key = lambda x:(x[0],x[1],x[2]))
            return hubo[0][1], hubo[0][2], hubo[0][3] # 해당 바다 위치와 도착 후 바라보는 방향 return
    return -1,-1,-1 # 아직 고래가 방문하지 않은 바다를 못만난다면 -1 return


def change(direction): # 다루기 편하게 방향 바꿔주기
    if direction == 1:
        return 3
    elif direction == 2:
        return 1
    elif direction == 3:
        return 0
    elif direction == 4:
        return 2




# 초기 설정
n,tr,tc,td = map(int,input().split()) # 격자크기, 고래의 시작 위치, 처음 바라보는 방향
tr -= 1 # 1-based 니까 빼주자
tc -= 1
td = change(td) # 방향도 내가 맞춘대로 바꿔주기

already_go = [[0] * n for _ in range(n)] # 이미 간 바다 체크
already_go[tr][tc] = 1 # 시작 위치는 이미 갔다고 생각
board = []
for i in range(n):
    board.append(list(map(int,input().split())))
custom_print("초기 바다 상태", board)

result = [(tr+1,tc+1)] # result : 이미 갔다간 바다 순서대로 들어있는 배열/ 시작위치는 처음부터 넣기
while True:
    # 거북이 이동

    tr,tc,td = move_turtle() # 최종으로 이동한 곳 업데이트

    custom_print("거북이 갈 수 있을 때까지 갔나", already_go)

    # 인접한 바다 찾기
    
    tr,tc,td = find_sea(tr,tc,already_go)
    if tr == -1: # 인접한 바다를 못찾으면 == 이미 다 갔다면 while 문 종료
        break
    result.append((tr+1,tc+1)) # 인접한 바다로 이동했으면 result 에 넣어주기
    already_go[tr][tc] = 1

# 결과 출력
for r,c in result:
    print(r,c)