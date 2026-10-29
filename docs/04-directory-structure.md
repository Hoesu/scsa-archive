# 04. 폴더 구조와 네이밍 규칙

여러 플랫폼(Codetree, SWEA, Programmers, 백준 …)에서 모은 문제를 **한 가지 규칙**으로 정리하는 방법입니다.

## 한눈에 보기

```
problems/
└── <플랫폼>/                          codetree | swea | programmers | boj | jungol | leetcode | etc
    └── <문제id>-<영문-slug>/          예) 12906-same-numbers, 1206-view, maze-escape
        ├── README.md                  메타데이터(front matter) + 요약 + 힌트
        └── solutions/
            ├── <github-id>.py                예) Hoesu.py
            └── <github-id>_<설명>.py         예) Hoesu_dfs.py
```

## 왜 이렇게 정했나요?

### 1. 1단계는 "플랫폼", 2단계는 "문제" — 경로가 절대 바뀌지 않도록

| 후보 | 문제점 |
|---|---|
| `난이도/유형/문제` | 난이도·유형은 **사람마다 의견이 다르고 바뀔 수 있음**. 폴더를 옮기면 링크가 깨지고 PR 충돌이 남 |
| `유형/문제` | 한 문제가 BFS 이면서 시뮬레이션이기도 함 → **어느 폴더에 넣을지 애매** |
| `주차/문제` | 같은 문제가 다른 주차에 다시 나오면 중복 |
| **`플랫폼/문제id`** ✅ | 문제의 **변하지 않는 속성**만 경로에 사용 → 위치가 유일하고 영구적 |

난이도, 유형(태그), 주차처럼 **바뀔 수 있는 정보는 README 의 메타데이터**에 적습니다.
여러 기준으로 보는 기능은 [PROBLEMS.md](https://github.com/Hoesu/scsa-archive/blob/index/PROBLEMS.md) (`index` 브랜치에 자동 생성) 가 플랫폼별·태그별로 제공합니다.

### 2. 문제 하나 = 폴더 하나, 풀이는 사람별 파일

- 같은 문제의 풀이가 한 폴더에 모여 있어서 **다른 사람 풀이와 비교**하기 쉽습니다.
- 파일명이 GitHub ID 라서 **서로 다른 사람의 PR 이 같은 파일을 건드릴 일이 없습니다** → 머지 충돌 최소화.

### 3. 폴더명은 영문 소문자·숫자·하이픈만

- 한글/공백/대문자 경로는 Windows·macOS 간 대소문자 처리, 터미널 입력, URL 인코딩에서 문제가 생깁니다.
- 숫자 id 를 앞에 두면 정렬이 쉽고, 영문 slug 를 뒤에 붙이면 폴더명만 보고도 어떤 문제인지 알 수 있습니다.

## 플랫폼별 id 정하는 법

| 플랫폼 | 폴더 key | id 로 쓸 값 | URL 예시 → 폴더명 |
|---|---|---|---|
| Programmers | `programmers` | URL 의 `lessons/` 뒤 숫자 | `.../lessons/12906` → `12906-same-numbers` |
| SW Expert Academy | `swea` | 문제 제목 앞의 번호 | `1206. [S/W 문제해결 기본] 1일차 - View` → `1206-view` |
| Codetree | `codetree` | 번호가 없으므로 URL 의 **마지막 영문 이름** | `.../problems/maze-escape/...` → `maze-escape` |
| 백준 | `boj` | 문제 번호 | `acmicpc.net/problem/1000` → `1000-a-plus-b` |
| JUNGOL (정올) | `jungol` | 문제 번호 | `jungol.co.kr/problem/1000` → `1000-a-plus-b` |
| LeetCode | `leetcode` | 문제 번호 | `1. Two Sum` → `1-two-sum` |
| 그 외 | `etc` | 출처를 알 수 있는 영문 id | `kakao-2023-emoticon` |

> **SWEA 주의**: 접속 URL 의 `contestProbId=AV5LrsUaDxcDFAXc` 같은 긴 값이 아니라 **화면에 보이는 문제 번호**(1206)를 씁니다.
> **slug 짓기**: 영어 제목이 있으면 그것을, 없으면 핵심을 2~4단어 영어로. 너무 고민하지 마세요. id 가 유일성을 보장합니다.

새 플랫폼을 추가하려면 `scripts/common.py` 의 `PLATFORMS`, `scripts/setup_labels.py`, `.github/labeler.yml` 을 함께 수정하는 PR 을 올려주세요.

## README.md 메타데이터 (front matter)

문제 README 맨 위의 `---` 사이 영역은 **스크립트가 읽는 데이터**입니다. 형식을 꼭 지켜주세요.

```yaml
---
title: 같은 숫자는 싫어                 # 원문 제목 그대로
platform: programmers                   # 상위 폴더명과 같아야 함
id: 12906                               # 폴더명이 이 값으로 시작해야 함
url: https://school.programmers.co.kr/learn/courses/30/lessons/12906
level: Lv.1                             # 플랫폼에 표기된 레벨 그대로
difficulty: 1                           # 공통 난이도 1~5 (아래 표)
tags: [스택/큐, 구현]                   # 대괄호 리스트, 쉼표 구분
proposer: Hoesu                         # 등록한 사람 GitHub ID
added: 2026-10-29                       # 등록일
---
```

| 키 | 필수 | 검사 내용 |
|---|:---:|---|
| `title`, `level`, `proposer` | ✅ | 비어 있지 않음 |
| `platform` | ✅ | 상위 폴더명과 일치 |
| `id` | ✅ | 폴더명이 `<id>` 또는 `<id>-...` |
| `url` | ✅ | `http(s)://` 로 시작 |
| `difficulty` | ✅ | 1~5 정수 |
| `tags` | ✅ | `[a, b]` 형식 리스트 |
| `added` 등 기타 키 | | 자유롭게 추가 가능 (예: `source: 2023 KAKAO BLIND`) |

## 공통 난이도 기준표

플랫폼마다 레벨 체계가 달라서, 비교·정렬을 위해 **1~5 공통 난이도**를 함께 기록합니다.
아래는 **대략적인 가이드**일 뿐이니 체감 난이도로 정하고, 이견이 있으면 리뷰에서 조정하세요.

| 공통 | 의미 | Programmers | SWEA | 백준 (solved.ac) | Codetree |
|:---:|---|---|---|---|---|
| 1 | 입문 — 문법, 단순 구현 | Lv.0 ~ Lv.1 | D1 ~ D2 | Bronze | Novice |
| 2 | 기초 — 정렬, 완전탐색, 기본 자료구조 | Lv.1 ~ Lv.2 | D3 | Silver | Novice High ~ Intermediate Low |
| 3 | 중급 — BFS/DFS, DP, 이분 탐색, 그리디 | Lv.2 | D4 | Gold 5 ~ 3 | Intermediate |
| 4 | 상급 — 복합 시뮬레이션, 최단 경로, 고급 DP | Lv.3 | D5 ~ D6 | Gold 2 ~ Platinum 5 | Intermediate High ~ 삼성 기출 |
| 5 | 최상급 — 고급 자료구조/알고리즘 | Lv.4 ~ Lv.5 | D7 ~ D8 | Platinum 4 이상 | Advanced |

> 삼성 SW 역량테스트 관점의 대략적 기준: **A형 ≈ 3~4**, **B형(Pro) ≈ 4~5**

## 태그 작성 가이드

검색과 PROBLEMS.md 의 "태그별 보기" 품질을 위해 **아래 표준 태그를 우선** 사용하세요. (필요하면 새 태그도 OK)

`구현` `시뮬레이션` `완전탐색` `백트래킹` `BFS` `DFS` `그래프` `최단경로` `트리` `유니온파인드`
`DP` `그리디` `정렬` `이분탐색` `투포인터` `슬라이딩윈도우` `누적합` `스택/큐` `우선순위큐` `해시`
`문자열` `수학` `비트마스킹` `분할정복` `세그먼트트리` `위상정렬` `MST`

- 한 문제당 1~3개가 적당합니다.
- 띄어쓰기 없이 위 표기 그대로 써야 같은 태그로 묶입니다. (`DP` ≠ `dp` ≠ `동적계획법`)

## 풀이 파일 규칙

| 규칙 | 예 |
|---|---|
| `<github-id>.py` | `Hoesu.py` |
| 같은 사람의 추가 풀이: `<github-id>_<설명>.py` (설명은 소문자/숫자/하이픈) | `Hoesu_dp.py`, `Hoesu_two-pointer.py` |
| 언어 | **파이썬만** (`.py`) |
| 파일 맨 위에 템플릿 헤더 | 결과, 접근, 회고 (복잡도는 선택) |

입출력 예제 파일(SWEA `sample_input.txt` 등)은 플랫폼 저작물이므로 저장소에 올리지 않습니다.

---

다음: [05. GitHub 기능 둘러보기](05-github-features.md)
