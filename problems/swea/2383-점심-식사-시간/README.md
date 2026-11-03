---
title: 점심 식사 시간
platform: swea
id: 2383
url: https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5-BEE6AK0DFAVl
level: 상급
difficulty: 4
tags: [완전탐색, 시뮬레이션]
proposer: Hyunnniiii
added: 2026-11-03
---

# 점심 식사 시간

> 원문: [swea 2383](https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5-BEE6AK0DFAVl) · 레벨 `상급` · 공통 난이도 `4`

## 문제 요약

배열 내 사람들과 계단 2개의 위치/길이 정보가 주어진다.
각 사람마다 두 계단 중 하나를 골라 내려갈 때, 모든 사람이 계단을 다 내려가는 데 걸리는 시간의 최솟값을 구하는 문제.

## 이 문제를 추천하는 이유

이번 1차 시험 문제와 유사하다.
계단 위치에 사람들이 들어갈 때, 계단 내 상태에 따라 투입 시점을 결정해야 한다.

## 핵심 포인트 / 함정

- 계단 입구에 도착한 뒤 **1분 후**부터 내려갈 수 있다.
- 한 계단에는 **최대 3명**까지만 동시에 내려갈 수 있고, 나머지는 입구에서 대기한다.
- 앞사람이 다 내려간 그 순간에 바로 대기자가 들어갈 수 있는지, 시간 경계 처리를 꼼꼼히 확인해야 한다.

<details>
<summary>힌트 1 (펼쳐서 보기)</summary>

각 위치의 사람들을 굳이 구분할 필요는 없다.

</details>

<details>
<summary>힌트 2</summary>

한 계단을 이미 3명이 이용 중이라면, 그중 가장 먼저 들어간 사람이 언제 나가는지만 확인하면 된다.

</details>
