"""
[Programmers 64063] 호텔 방 배정
https://school.programmers.co.kr/learn/courses/30/lessons/64063

작성자 : @Zon1t
결과   : 통과 (실행 시간 XX ms, 메모리 XX KB)
복잡도 : (선택) 시간 O( ), 공간 O( )
접근   :
  - k가 10^12 ?? 이건 딕셔너리 써야겠는데?
  - 투숙객 수는 20만 이하. 그럼 그냥 순회하면서 적절히 배치하면 되겠다.
회고   :
  - 익숙하게 parent 찾는 find 함수가 아니라 다음 방을 지칭해야 하므로, 해당 부분에 많은 고민을 해야한다!
"""
# 방 할당 문제
# 시간초과 자꾸 남
# recursion -> while
def solution(k, room_number):
    answer = []

    parent = dict() # 쓴 애들

    def find(num):

        child = num
        par = parent.get(child, 0)
        while par:
            child = par
            par = parent.get(child, 0)

        parent[child] = child + 1
        start = num
        par = child
        while start != par:
            #print(start, par)
            parent[start], start = par, parent.get(start, 0)

        return child

    for room in room_number:
        res = find(room)
        answer.append(res)
        #print(f"for room{room} => {res}\n {parent} ")

    return answer