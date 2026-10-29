# 02. 풀이 제출

등록된 문제를 풀었다면 **브랜치 → 커밋 → PR → 리뷰 → 머지** 순서로 올립니다.
아직 등록되지 않은 문제라면 [01. 문제 제안·등록](01-propose-problem.md)을 먼저 보세요.

## 1. 브랜치 만들기

```bash
git switch main
git pull
git switch -c solve/<내아이디>/programmers-12906
```

> **왜 브랜치를 쓰나요?** `main` 은 모두가 공유하는 "정본" 입니다. 각자 브랜치에서 작업하고,
> 리뷰를 거친 것만 `main` 에 합치면 서로의 작업이 섞이거나 망가지지 않습니다.

## 2. 풀이 파일 만들기

```bash
python scripts/new_solution.py problems/programmers/12906-same-numbers --author <내아이디>
```

`problems/programmers/12906-same-numbers/solutions/<내아이디>.py` 가 헤더와 함께 생성됩니다.

| 상황 | 파일명 | 명령 |
|---|---|---|
| 기본 | `hoesu.py` | (옵션 없음) |
| 다른 방법으로 한 번 더 풀었다 | `hoesu_dp.py` | `--variant dp` |

> 이 저장소는 **파이썬 풀이만** 받습니다. `.py` 가 아닌 파일은 자동 검사에서 실패합니다.

### 헤더 작성하기

리뷰어가 코드를 읽기 전에 의도를 파악할 수 있도록, 헤더를 꼭 채워주세요.

```python
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
```

- **결과**: 시간 초과/오답이 난 풀이도 환영합니다! `실패 (시간 초과)` 라고 적고 리뷰에서 도움을 받으세요.

## 3. 검사하고 커밋하기

```bash
python scripts/validate.py
git status                       # 내가 바꾼 파일만 있는지 확인
git add problems/programmers/12906-same-numbers/solutions/
git commit -m "solve: programmers 12906 같은 숫자는 싫어"
git push -u origin solve/<내아이디>/programmers-12906
```

## 4. Pull Request 만들기

1. 푸시 후 GitHub 저장소에 들어가면 노란 배너의 **Compare & pull request** 클릭
2. 제목: `[풀이] programmers/12906 같은 숫자는 싫어`
3. 템플릿의 **풀이 요약**과 **리뷰어에게 특히 봐줬으면 하는 부분**을 채웁니다
4. 오른쪽 **Reviewers** 에서 리뷰받고 싶은 사람을 1~2명 지정 (선택)
5. 아직 작성 중이라면 **Create draft pull request** 로 만들 수 있어요

PR 을 만들면 자동으로:
- `validate` 검사가 돌아갑니다. ❌ 가 뜨면 **Details** 를 눌러 원인을 확인하세요.
- 경로를 보고 `풀이`, `platform:programmers` 같은 **라벨이 자동으로** 붙습니다.

## 5. 리뷰 반영하기

리뷰 코멘트가 달리면 같은 브랜치에서 수정 후 다시 푸시하면 PR 에 자동으로 반영됩니다.

```bash
# 코드 수정 후
git add .
git commit -m "solve: 리뷰 반영 - 변수명 정리"
git push
```

- 반영한 코멘트에는 "반영했습니다! (커밋 abc1234)" 처럼 답하고 **Resolve conversation** 을 누릅니다.
- 리뷰어가 **Suggested change** 를 달았다면 **Commit suggestion** 버튼으로 바로 반영할 수 있어요.
- 동의하지 않는 의견에는 이유를 들어 답해도 괜찮습니다. 토론도 리뷰의 일부입니다.

## 6. 머지하기

**승인(Approve) 1개 이상 + 검사 통과**가 되면 **PR 작성자 본인이** 머지합니다.

1. **Squash and merge** 선택 (커밋 여러 개를 하나로 합쳐 `main` 기록을 깔끔하게 유지)
2. **Delete branch** 클릭
3. 로컬 정리:

```bash
git switch main
git pull
git branch -d solve/<내아이디>/programmers-12906
```

몇 분 뒤 [PROBLEMS.md](https://github.com/Hoesu/scsa-archive/blob/index/PROBLEMS.md) 의 풀이 수와 기여 현황에 내 이름이 반영됩니다. 🎉

## 자주 하는 실수

| 증상 | 원인 / 해결 |
|---|---|
| `validate` 실패: 풀이 파일명 형식 | 파일명에 공백, 한글, 점(`.`)이 들어갔는지 확인 |
| `validate` 경고: PR 작성자와 다름 | 파일명은 **본인 GitHub ID** 여야 합니다 |
| PR 에 남의 파일 변경이 섞여 있음 | 오래된 브랜치에서 작업한 경우. [Git 치트시트](06-git-cheatsheet.md#main-최신-내용을-내-브랜치에-반영하기) 참고 |
| `main` 에서 커밋해버렸다 | [Git 치트시트](06-git-cheatsheet.md#실수로-main-에-커밋했어요) 참고 |

---

다음: [03. 코드 리뷰](03-code-review.md)
