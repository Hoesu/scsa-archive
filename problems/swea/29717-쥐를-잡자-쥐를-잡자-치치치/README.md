---
title: 쥐를 잡자 쥐를 잡자 치치치
platform: swea
id: 29717
url: https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD6YOoqdaLHBISc&categoryId=AaD6YOoqdaLHBISc&categoryType=CODE
level: D3
difficulty: 4
tags: [시뮬레이션]
proposer: onyou-sub
added: 2026-11-02
---

# 쥐를 잡자 쥐를 잡자 치치치

> 원문: [swea 29717](https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD6YOoqdaLHBISc&categoryId=AaD6YOoqdaLHBISc&categoryType=CODE) · 레벨 `D3` · 공통 난이도 `4`

## 문제 요약

N×N 정원(빈칸 0 / 돌 -1 / 낙엽 1 이상)에 고양이 치치와 쥐 M마리가 있다.
하루는 **낮: 치치 이동·포획 → 밤: 쥐 이동 → 낙엽 확산 → 바람(낙엽 감소)** 순으로 진행된다.
치치는 돌을 피해 가장 가까운 쥐에게 1칸 다가가 잡고, 쥐는 가장 가까운 낙엽 칸으로 1칸 이동해 숨는다.
T일 안에 모든 쥐를 잡으면 걸린 일 수와 잡힌 쥐 번호 순서를, 못 잡으면 -1을 출력한다.

## 이 문제를 추천하는 이유

27기에서 직접 제작한 문제.

## 핵심 포인트 / 함정

- 치치는 돌을 지날 수 없지만, 쥐는 돌 칸으로도 이동할 수 있다. 쥐는 치치나 다른 쥐가 있는 칸으로는 못 간다.
- 치치의 목표 쥐: 최단거리 → r 큰 순 → c 큰 순. 이동 방향과 쥐의 이동 방향은 모두 상 → 우 → 하 → 좌 우선.
- 낙엽 칸에 있는 쥐는 치치가 같은 칸에 와도 잡히지 않고, 이미 낙엽에 숨은 쥐는 이동하지 않는다.
- 낙엽 확산은 **동시에** 일어나며, 낙엽이 없는 인접 빈칸마다 `L / 5`(몫)씩 퍼지고 원래 칸은 퍼진 만큼 줄어든다.
- 바람으로 낙엽이 0이 된 칸은 빈칸이 되고, 모든 쥐가 잡히는 순간 즉시 종료된다.

<details>
<summary>힌트 1 (펼쳐서 보기)</summary>

치치와 쥐 모두 "목표까지의 최단거리가 줄어드는 방향"으로 1칸 움직인다. 목표 쪽에서 BFS를 한 번 돌려 거리 맵을 만들면, 현재 칸의 상·우·하·좌 중 거리가 1 작은 칸을 우선순위대로 고르면 된다.

</details>

<details>
<summary>힌트 2</summary>

낙엽 확산은 원본 격자를 보면서 변화량을 별도 배열에 모았다가 한 번에 반영하자. 바로 갱신하면 같은 날 새로 생긴 낙엽이 다시 퍼지는 실수가 생긴다.

</details>
