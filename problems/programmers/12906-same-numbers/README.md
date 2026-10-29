---
title: 같은 숫자는 싫어
platform: programmers
id: 12906
url: https://school.programmers.co.kr/learn/courses/30/lessons/12906
level: Lv.1
difficulty: 1
tags: [스택/큐, 구현]
proposer: Hoesu
added: 2026-10-29
---

# 같은 숫자는 싫어

> 원문: [programmers 12906](https://school.programmers.co.kr/learn/courses/30/lessons/12906) · 레벨 `Lv.1` · 공통 난이도 `1`

## 문제 요약

0~9로 이루어진 정수 배열이 주어질 때, **연속해서 같은 숫자가 나오면 하나만 남기고** 나머지를 지운 배열을 반환한다.
원래 순서는 유지해야 한다.

## 이 문제를 추천하는 이유

- 스택의 "마지막 원소와 비교" 패턴을 익히기 좋은 입문 문제
- 저장소 사용법(문제 등록 → 풀이 PR → 리뷰)을 연습하기 위한 **예시 문제**이기도 합니다

## 핵심 포인트 / 함정

- "전체에서 중복 제거"가 아니라 "**연속된** 중복 제거"다. `set` 을 쓰면 틀린다.
- 배열 길이가 최대 1,000,000 이므로 O(N) 으로 풀어야 한다.

<details>
<summary>힌트 1 (펼쳐서 보기)</summary>

결과 배열의 마지막 원소만 알면 된다.

</details>

<details>
<summary>힌트 2</summary>

새 숫자가 결과 배열의 마지막 원소와 다를 때만 추가한다.

</details>
