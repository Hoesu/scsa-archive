# 02. 풀이 제출

등록된 문제를 풀었다면 풀이를 PR 로 올립니다. **누가 등록한 문제든 상관없어요.**

**한눈에 보기**

```bash
git switch main
python scripts/new_solution.py 같은숫자        # ① 최신화 + 문제 검색 + 브랜치 + 풀이 파일 생성
# ② solutions/<내아이디>.py 에 헤더와 코드 작성
python scripts/validate.py                     # ③ 검사
git add problems/
git commit -m "[풀이] 같은 숫자는 싫어"
git push -u origin solve/<내아이디>/programmers-12906
# ④ GitHub 에서 PR → 리뷰 → 머지
```

> [!TIP]
> 뭘 풀지 고민된다면 [전체 문제 목록](https://github.com/Hoesu/scsa-archive/blob/index/PROBLEMS.md) 맨 위의 **풀이를 기다리는 문제** 부터 보세요.
> 아직 등록되지 않은 문제라면 [01. 문제 제안·등록](01-propose-problem.md) 이 먼저입니다.

## 1. 풀이 파일 만들기

`main` 브랜치에서 풀 문제의 **이름 일부**를 넣어 실행합니다.

```bash
git switch main
python scripts/new_solution.py 같은숫자
```

스크립트가 알아서 해주는 것:

- **최신화**: `main` 을 최신으로 받습니다. (`git pull`)
- **GitHub ID**: 처음 한 번만 묻고 기억합니다. (바꾸려면 `git config scsa.author <새 ID>`)
- **문제 찾기**: 제목·번호·폴더 이름 일부로 검색합니다. 여러 개가 맞으면 번호로 고르게 해줘요.
- **브랜치**: `solve/<내아이디>/<플랫폼>-<번호>` 브랜치를 만들고 이동합니다.
- **풀이 파일**: `solutions/<내아이디>.py` 를 헤더와 함께 만듭니다.
  이미 내 풀이가 있으면 두 번째 풀이의 구분 이름(예: `dp` → `<내아이디>_dp.py`)을 물어봐요.
- **다음 명령**: 문제 제목과 브랜치 이름이 채워진 커밋·푸시 명령을 출력합니다.

<details>
<summary>검색은 어떻게 동작하나요?</summary>

띄어쓰기, 하이픈(`-`), 대소문자는 무시합니다.

| 입력 예 | 결과 |
|---|---|
| `같은숫자`, `아기 고래` | 하나만 맞으면 "이 문제가 맞나요?" 확인 후 진행 |
| `벨트`, `codetree` | 여러 개가 맞으면 번호 목록에서 고르기 |
| `12906` | 번호를 정확히 치면 바로 그 문제 |
| (아무것도 안 넣음) | 전체 목록에서 고르기. 풀이가 없는 문제가 먼저 나와요 |
| 맞는 게 없음 | 다시 검색하거나 Enter 로 전체 목록 보기 |

</details>

> [!NOTE]
> **왜 브랜치를 쓰나요?** `main` 은 모두가 공유하는 "정본" 입니다. 각자 브랜치에서 작업하고 리뷰를 거친 것만 `main` 에 합치면, 서로의 작업이 섞이거나 망가지지 않습니다.

## 2. 헤더와 코드 작성하기

파일 맨 위 헤더를 채우면 리뷰어가 코드를 읽기 전에 의도를 파악할 수 있어요.

```python
"""
[Programmers 12906] 같은 숫자는 싫어
https://school.programmers.co.kr/learn/courses/30/lessons/12906

작성자 : @Hoesu
결과   : 통과
복잡도 : (선택) 시간 O(N), 공간 O(N)
접근   :
  - 결과 리스트를 스택처럼 사용한다.
  - 현재 숫자가 스택의 top 과 다를 때만 push 한다.
회고   :
  - 처음에 set 으로 중복을 지우려다 "연속" 조건을 놓칠 뻔했다.
"""
```

| 항목 | 필수 | 설명 |
|---|:---:|---|
| 결과 | ✅ | 통과/실패. **시간 초과·오답 풀이도 환영!** `실패 (시간 초과)` 라고 적고 리뷰에서 도움을 받으세요 |
| 접근 | ✅ | 핵심 아이디어 1~3줄 |
| 복잡도 | | 선택. 어려우면 비워두거나 줄을 지워도 됩니다 |
| 회고 | | 선택. 헤맨 부분, 배운 점 |

> [!WARNING]
> 이 저장소는 **파이썬 풀이만** 받습니다. `.py` 가 아닌 파일은 자동 검사에서 실패합니다.

## 3. 검사 → 커밋 → 푸시

1번 스크립트가 마지막에 출력한 명령을 그대로 실행하면 됩니다.

```bash
python scripts/validate.py       # "에러 0개" 확인
git status                       # 내가 바꾼 파일만 있는지 확인
git add problems/
git commit -m "[풀이] 같은 숫자는 싫어"
git push -u origin solve/<내아이디>/programmers-12906
```

## 4. PR 만들기

1. 푸시 후 GitHub 저장소 페이지에 뜨는 **Compare & pull request** 클릭
2. 제목 확인: `[풀이] 같은 숫자는 싫어` (커밋 메시지대로 이미 채워져 있어요)
3. 본문에서 **PR 유형**과 **체크리스트**를 체크
4. (선택) 오른쪽 **Reviewers** 에 리뷰받고 싶은 사람 지정
5. **Create pull request** — 아직 작성 중이면 **Create draft pull request**

PR 을 만들면 자동으로 `validate` 검사가 돌고, `풀이`, `platform:programmers` 같은 라벨이 붙습니다.
검사에 ❌ 가 뜨면 **Details** 를 눌러 원인을 확인하세요.

## 5. 리뷰 반영하기

같은 브랜치에서 고쳐서 다시 푸시하면 PR 에 자동으로 반영됩니다.

```bash
git add problems/
git commit -m "[풀이] 리뷰 반영 - 변수명 정리"
git push
```

- 반영한 코멘트에는 "반영했습니다!" 처럼 답하고 **Resolve conversation** 을 누릅니다.
- **Suggested change** 는 **Commit suggestion** 버튼으로 바로 반영할 수 있어요.
- 동의하지 않는 의견에는 이유를 들어 답해도 괜찮습니다. 토론도 리뷰의 일부예요.

## 6. 머지와 정리

**승인 1개 이상 + 검사 통과**가 되면 **PR 작성자 본인이** 머지합니다.

1. **Squash and merge** → **Confirm**
2. **Delete branch**
3. 내 컴퓨터 정리:

```bash
git switch main
git pull
git branch -D solve/<내아이디>/programmers-12906
```

몇 분 뒤 [전체 문제 목록](https://github.com/Hoesu/scsa-archive/blob/index/PROBLEMS.md) 의 풀이 수와 기여 현황에 반영됩니다. 🎉

## 자주 하는 실수

| 증상 | 원인 / 해결 |
|---|---|
| `validate` 실패: 풀이 파일명 형식 | 파일명에 공백, 한글, 점(`.`)이 들어갔는지 확인 |
| `validate` 경고: PR 작성자와 다름 | 파일명은 **본인 GitHub ID** 여야 합니다. `git config scsa.author` 확인 |
| 검색해도 문제가 안 나옴 | `main` 이 아닌 브랜치에서 실행하면 최신화를 건너뜁니다. `git switch main` 후 다시 실행 |
| PR 에 남의 파일 변경이 섞여 있음 | 오래된 브랜치에서 작업한 경우. [Git 치트시트](06-git-cheatsheet.md#main-최신-내용을-내-브랜치에-반영하기) 참고 |
| `main` 에서 커밋해버렸다 | [Git 치트시트](06-git-cheatsheet.md#실수로-main-에-커밋했어요) 참고 |

---

[← 01. 문제 제안·등록](01-propose-problem.md) · [📚 문서 목록](../README.md#문서-안내) · [03. 코드 리뷰 →](03-code-review.md)
