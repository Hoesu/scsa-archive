# 01. 문제 제안·등록

좋은 문제를 발견했다면 **Issue 로 제안**하고, 채택되면 **PR 로 등록**합니다.
제안과 등록을 나누는 이유는 중복 등록을 막고, 반 전체가 "어떤 문제를 같이 풀지" 논의할 기회를 만들기 위해서입니다.

## 1단계. 중복 확인

- [PROBLEMS.md](https://github.com/Hoesu/scsa-archive/blob/index/PROBLEMS.md) 에서 `Ctrl+F` 로 번호/제목 검색
- [Issues](https://github.com/Hoesu/scsa-archive/issues?q=label%3A문제-제안) 에서 열린/닫힌 제안 검색

## 2단계. Issue 로 제안하기

1. **Issues → New issue → `문제 제안`** 템플릿 선택
2. 플랫폼, 번호, 링크, 레벨, 체감 난이도, 태그, **추천 이유**를 채웁니다
3. 제목은 미리 들어가 있는 `[제안]` 뒤에 **문제 이름만** 자유롭게 적으면 됩니다. 예) `[제안] 같은 숫자는 싫어`
   (플랫폼·번호는 아래 칸에 따로 적으니 제목에 넣지 않아도 돼요)
4. **Submit new issue**

> **좋은 추천 이유의 예**
> - "삼성 A형 기출 유형인 시뮬레이션 + BFS 조합이라 연습하기 좋아요"
> - "투 포인터 입문 문제로 딱이에요. 처음에 O(N²) 으로 풀면 시간 초과가 나서 개선을 경험할 수 있어요"

## 3단계. 채택

- 다른 사람들은 마음에 드는 제안에 👍 리액션을 남깁니다.
- **👍 3개 이상** 또는 운영진 판단으로 `채택` 라벨이 붙습니다.
- 이미 있는 문제는 `중복`, 논의가 더 필요하면 `보류` 라벨이 붙습니다.
- 운영진은 채택된 문제를 이번 주 **Milestone** 에 넣기도 합니다. ([05 문서](05-github-features.md) 참고)

## 4단계. 문제 등록 PR

채택되면 제안자(또는 이슈에 "제가 할게요!" 댓글을 단 사람)가 등록합니다.
작업을 시작할 때 이슈 오른쪽 **Assignees** 에 자신을 지정하면 중복 작업을 막을 수 있어요.

```bash
git switch main && git pull
git switch -c problem/programmers-12906

python scripts/new_problem.py --issue <제안 이슈 번호>     # 예) --issue 12
```

`--issue` 를 주면 **제안 이슈에 적힌 정보를 그대로 가져옵니다.** 플랫폼, 번호, 제목, 링크, 레벨, 난이도, 태그, 제안자, 추천 이유를 다시 입력할 필요가 없어요.
번호가 숫자인 문제는 폴더명에 쓸 영문 slug 하나만 물어봅니다. (예: `same-numbers`, 생략 가능)
스크립트가 마지막에 커밋 메시지와 `Closes #번호` 까지 알려줍니다.

> 이슈 없이 등록하려면 `python scripts/new_problem.py` 만 실행하세요. 질문에 차례로 답하면 됩니다.

생성된 `problems/<플랫폼>/<id>-<slug>/README.md` 를 열어 아래를 **직접** 작성합니다.

| 섹션 | 작성 요령 |
|---|---|
| 문제 요약 | 입력/출력이 무엇인지 2~4줄. **원문 복사 금지** |
| 추천 이유 | 이슈에서 자동으로 들어옵니다. 필요하면 다듬기 |
| 핵심 포인트 / 함정 | 제한 조건, 엣지 케이스. 정답을 직접 말하지는 않기 |
| 힌트 1, 2 | 접힌 블록(`<details>`) 안에 단계적으로 |

예시: [`problems/programmers/12906-same-numbers/README.md`](../problems/programmers/12906-same-numbers/README.md)

```bash
python scripts/validate.py
git add problems/
git commit -m "[문제] 같은 숫자는 싫어"
git push -u origin problem/programmers-12906
```

GitHub 에서 PR 을 만들 때:
- 제목: `[문제] 같은 숫자는 싫어` (커밋 메시지를 이 형식으로 썼다면 이미 채워져 있어요)
- 본문의 `Closes #` 뒤에 **제안 이슈 번호**를 적습니다 → 머지되면 이슈가 자동으로 닫힙니다.
- 본인 풀이도 있다면 같은 PR 에 포함해도 됩니다.

## 스크립트 없이 수동으로 만들기

스크립트를 쓸 수 없는 환경이라면 [`templates/problem.md`](../templates/problem.md) 를 복사해서
`problems/<플랫폼>/<폴더명>/README.md` 로 저장하고 `{{...}}` 부분을 채우면 됩니다.
`solutions/` 폴더는 풀이 파일을 넣을 때 만들어도 됩니다.

---

다음: [02. 풀이 제출](02-submit-solution.md)
