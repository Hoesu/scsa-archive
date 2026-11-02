---
title: 메롱메롱 개구리와 파리의 우당탕탕 대소동
platform: swea
id: 29706
url: https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD6W7R6kFPHBIPk&categoryId=AaD6W7R6kFPHBIPk&categoryType=CODE
level: D3
difficulty: 4
tags: [시뮬레이션]
proposer: jiho092
added: 2026-11-02
---

# 메롱메롱 개구리와 파리의 우당탕탕 대소동

> 원문: [swea 29706](https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD6W7R6kFPHBIPk&categoryId=AaD6W7R6kFPHBIPk&categoryType=CODE) · 레벨 `D3` · 공통 난이도 `4`

## 문제 요약

N×N 연못(물 0 / 연잎 1)에 개구리 T마리와 파리 F마리가 있다. 처음엔 1번 개구리만 깨어 있다.
매 턴 **개구리 행동(번호 순) → 파리 이동 → 식곤증 카운트 감소**가 진행된다.
깨어 있는 개구리는 거리 L 이내 파리를 모두 먹고, 정확히 L+1 거리의 잠든 개구리를 깨운다.
파리를 먹었다면 연잎이 가라앉아 가장 가까운 빈 연잎으로 점프(없으면 익사)하고 번호만큼 식곤증에 빠진다.
K턴 동안 먹은 파리의 총 수를 구한다.

## 이 문제를 추천하는 이유

27기가 직접 제작한 문제.

## 핵심 포인트 / 함정

- 개구리 상태가 **깊은 잠 / 깨어 있음 / 식곤증 / 사망** 으로 나뉜다. 침 범벅은 *깊은 잠* 개구리만 깨운다.
- 이번 턴에 깨어난 개구리는 **다음 턴부터** 먹을 수 있다.
- 파리를 0마리 먹으면 침수·점프·식곤증 모두 생략.
- 대피 위치는 **개구리가 없는 연잎** 중 맨해튼 거리 최소 → 행 → 열 순.
- 파리는 벽에 닿으면 방향을 뒤집고 **같은 턴에 1칸 이동**한다. 같은 칸에 여러 마리가 겹칠 수 있다.

<details>
<summary>힌트 1 (펼쳐서 보기)</summary>

개구리마다 `위치`, `상태`, `남은 식곤증 턴`을 함께 관리해 보자. 한 턴 안에서 단계 순서(개구리 → 파리 → 수면 감소)를 그대로 따라가면 된다.

</details>

<details>
<summary>힌트 2</summary>

파리는 `(행, 열, 방향)` 목록으로 들고 있으면 편하다. 개구리가 먹은 파리는 목록에서 제거하고, 살아남은 파리만 이동시키자.

</details>
