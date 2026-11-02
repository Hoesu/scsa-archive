---
title: 점령전
platform: swea
id: 29672
url: https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD28FJqwqXHBIPk&categoryId=AaD28FJqwqXHBIPk&categoryType=CODE
level: D4
difficulty: 4
tags: [시뮬레이션]
proposer: Hoesu
added: 2026-11-02
---

# 점령전

> 원문: [swea 29672](https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AaD28FJqwqXHBIPk&categoryId=AaD28FJqwqXHBIPk&categoryType=CODE) · 레벨 `D4` · 공통 난이도 `4`

## 문제 요약

N×N 격자(도로 0 / 벽 1)에 포탑 M개와 K개 팀의 플레이어 P명이 있다.
한 라운드는 **플레이어 이동 → 포탑 점령(난투극) → 포탑 공격** 순으로 진행되며, 최대 L라운드 동안 반복한다.
난투극 승리, 포탑 공격, 게임 종료 시 점령 포탑 수로 점수를 얻고, 각 팀의 최종 점수를 팀 번호 순으로 출력한다.

## 이 문제를 추천하는 이유

27기에서 직접 제작한 문제.

## 핵심 포인트 / 함정

- 이동: 도로 기준 최단거리가 가장 짧은 포탑이 목표(동률이면 탐색에서 먼저 발견된 포탑). 탐색·경로 우선순위는 **상 → 하 → 좌 → 우**.
- 한 라운드에 최대 이동 속도 s칸 이동하고, 포탑에 도착하면 즉시 멈춘다. 도달 가능한 포탑이 없으면 이동하지 않는다.
- 이미 점령된 포탑도 목표가 될 수 있다. 점령자는 이후 이동하지 않는다.
- 난투극은 **같은 팀끼리도** 싸운다. 기존 점령자도 참여하며, 전투력 최고 1명만 남고 그 팀이 제외된 인원당 1점.
- 공격: 다른 팀이면서 포탑 점령자가 아닌 플레이어 중 맨해튼 거리 최소 → 전투력 최소를 공격(벽 무시), 1명당 10점.
- 공격 대상은 STAGE 3 시작 시점 기준으로 **동시에** 정해지므로 여러 포탑이 같은 플레이어를 공격해도 각각 점수를 얻는다.
- 점령자를 제외한 플레이어가 0명이면 즉시 종료. 종료 시 점령 포탑 1개당 30점 추가.
- 좌표는 0-indexed. P는 최대 1,000명.

<details>
<summary>힌트 1 (펼쳐서 보기)</summary>

포탑은 최대 10개뿐이다. 플레이어마다 BFS를 돌리기보다 **포탑마다** 거리 맵을 만들어 두면, 플레이어는 맵을 조회만 해서 목표 포탑을 고를 수 있다. (단, 동률일 때 "먼저 발견된 포탑" 기준은 플레이어 위치에서의 탐색 순서임에 주의)

</details>

<details>
<summary>힌트 2</summary>

목표 포탑까지의 거리 맵이 있으면, 현재 칸에서 상·하·좌·우 중 거리가 1 작은 칸으로 한 칸씩 s번 옮기면 우선순위를 지킨 최단 경로 이동이 된다. 점령은 "포탑 칸별로 도착한 플레이어 + 기존 점령자"를 모아 한 번에 처리하자.

</details>
