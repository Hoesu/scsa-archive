---
title: 리코쳇 로봇
platform: programmers
id: 169199
url: https://school.programmers.co.kr/learn/courses/30/lessons/169199?gad_source=1&gad_campaignid=22356298761&gbraid=0AAAAAC_c4nDtlcqqydkNIAku5Cjs5iSfH&gclid=CjwKCAjwgJHXBhBGEiwAHohJq406kxXLW-M40qmcT3QjVvQFHThL-44RXSt1hphACQnUZLnMrtAzUhoCAU4QAvD_BwE
level: Lv.2
difficulty: 3
tags: [BFS, 시뮬레이션]
proposer: Hyunnniiii
added: 2026-11-02
---

# 리코쳇 로봇

> 원문: [programmers 169199](https://school.programmers.co.kr/learn/courses/30/lessons/169199?gad_source=1&gad_campaignid=22356298761&gbraid=0AAAAAC_c4nDtlcqqydkNIAku5Cjs5iSfH&gclid=CjwKCAjwgJHXBhBGEiwAHohJq406kxXLW-M40qmcT3QjVvQFHThL-44RXSt1hphACQnUZLnMrtAzUhoCAU4QAvD_BwE) · 레벨 `Lv.2` · 공통 난이도 `3`

## 문제 요약
로봇의 시작점, 목표 지점, 장애물이 표시된 격자판을 입력으로 받았을 때 목표 지점까지 도달하는 데 필요한 최소 이동 횟수를 구한다.


## 이 문제를 추천하는 이유
* 가능한 모든 경우를 탐색하는 백트래킹으로 생각할 수 있으나, BFS로 간단하게 해결할 수 있는 문제임.
* 일반적인 BFS와 이동 방식이 미묘하게 달라서 BFS 응용 연습에 좋음.


## 핵심 포인트 / 함정
* 한 칸 이동이 아니라, 가능한 만큼 모두 이동하는 것이 1회 이동
* 백트래킹으로 접근했을 때 시간초과가 발생할 가능성이 높다.

<details>
<summary>힌트 1 (펼쳐서 보기)</summary>

지나가는 경로 상의 모든 지점이 아닌, 멈추는 위치만 고려한다.


</details>

<details>
<summary>힌트 2</summary>

한 방향으로 갈 수 있는만큼 이동한 뒤, 멈춘 위치 좌표만 큐에 넣어준다.

</details>
