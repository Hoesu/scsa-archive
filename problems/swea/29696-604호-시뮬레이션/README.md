---
title: 604호 시뮬레이션
platform: swea
id: 29696
url: https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD5x0z6c-DHBISc&categoryId=AaD5x0z6c-DHBISc&categoryType=CODE
level: D3
difficulty: 4
tags: [시뮬레이션]
proposer: Zon1t
added: 2026-11-02
---

# 604호 시뮬레이션

> 원문: [swea 29696](https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD5x0z6c-DHBISc&categoryId=AaD5x0z6c-DHBISc&categoryType=CODE) · 레벨 `D3` · 공통 난이도 `4`

## 문제 요약

N×N 강의실에 'ㄹ'자 순서로 ID(1 ~ N²)가 매겨진 직원들이 있고, 각자 코딩 실력과 정신력을 가진다.
하루는 **아침: 난이도 K 문제 풀이 → 점심: 팀 편성 및 실력 상승 → 저녁: 자리 재배치** 순으로 진행된다.
T일 동안 매일 저녁 일과가 끝난 뒤 전체 직원의 코딩 실력 총합과 정신력 총합을 출력한다.

## 이 문제를 추천하는 이유

27기에서 직접 제작한 문제.

## 핵심 포인트 / 함정

- 아침: 실력 ≥ K면 실력 +1, 아니면 정신력이 `K - 실력`만큼 감소(최대 4). 정신력 0 이하가 되면 퇴실해 점심에서 제외된다.
- 점심: 남은 직원 정신력 +2 후 팀 편성. 상하좌우로 인접하고 실력 차가 D 이하이면 같은 팀이다.
- 1인 그룹은 ID가 작은 순서대로 인접 팀에 병합한다. 팀 평균과의 실력 차가 가장 작은 팀, 같으면 **우 → 하 → 좌 → 상** 순으로 고르고, 병합 결과는 즉시 반영된다.
- 병합 후에도 혼자인 직원이 있을 수 있고, 팀이 아예 없을 수도 있다.
- 실력 상승: 팀 평균 이상이면 +1, 아니면 +2. 모든 연산은 소수점 이하 버림.
- 저녁: 남은 직원이 'ㄹ'자 순서대로 앞자리부터 당겨 앉고, 퇴실자는 ID 순으로 뒷자리를 채우며 정신력이 10이 된다.
- 시간 제한: Python 기준 26개 테스트 케이스 합쳐 1초.

<details>
<summary>힌트 1 (펼쳐서 보기)</summary>

'ㄹ'자 순서 번호 ↔ (행, 열) 변환 함수를 먼저 만들어 두자. 저녁 재배치는 'ㄹ'자 순서로 직원 목록을 뽑아, 남은 직원 + 퇴실 직원(ID 순)을 이어 붙인 뒤 다시 'ㄹ'자 순서로 채우면 된다.

</details>

<details>
<summary>힌트 2</summary>

점심 팀 편성은 BFS로 그룹 번호 맵을 만들고, 그룹마다 인원 수와 실력 합을 따로 관리하자. 1인 그룹을 병합할 때는 그 직원의 그룹 번호와 해당 그룹의 인원·합만 갱신하면 즉시 반영이 된다.

</details>
