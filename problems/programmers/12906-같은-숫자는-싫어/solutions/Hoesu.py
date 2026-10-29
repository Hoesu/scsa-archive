"""
[Programmers 12906] 같은 숫자는 싫어
https://school.programmers.co.kr/learn/courses/30/lessons/12906

작성자 : @Hoesu
결과   : 통과
복잡도 : 시간 O(N), 공간 O(N)
접근   :
  - 결과 리스트를 스택처럼 사용한다.
  - 현재 숫자가 스택의 top 과 다를 때만 push 한다.
회고   :
  - 처음에 set 으로 중복을 지우려다 "연속" 조건을 놓칠 뻔했다.
"""


def solution(arr):
    answer = []
    for n in arr:
        if not answer or answer[-1] != n:
            answer.append(n)
    return answer
