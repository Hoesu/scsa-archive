# 기여 가이드

이 문서는 규칙의 **요약본**입니다. 단계별 설명은 각 링크를 따라가세요.

## 전체 흐름 한눈에 보기

```
 [문제 발굴]                 [문제 등록]                    [풀이 & 리뷰]
 Issue: 문제 제안  ──채택──▶  PR: 문제 폴더 추가  ──머지──▶  PR: 풀이 추가 ──리뷰/승인──▶ 머지
   (라벨: 문제-제안)           (Closes #이슈번호)              (누구나 언제든)
                                                                    │
                                              Actions 가 index 브랜치의 PROBLEMS.md 자동 갱신 ◀─┘
```

| 단계 | 누가 | 무엇을 | 가이드 |
|---|---|---|---|
| 1. 제안 | 누구나 | `문제 제안` 템플릿으로 Issue 작성 | [01](docs/01-propose-problem.md) |
| 2. 채택 | 운영진 또는 👍 3개 이상 | `채택` 라벨 부착 | [01](docs/01-propose-problem.md) |
| 3. 등록 | 제안자 (또는 지원자) | 문제 폴더 + README PR | [01](docs/01-propose-problem.md) |
| 4. 풀이 | 누구나 | 풀이 파일 PR | [02](docs/02-submit-solution.md) |
| 5. 리뷰 | 누구나 (1명 이상 승인 필요) | 코드 리뷰, Approve | [03](docs/03-code-review.md) |
| 6. 머지 | **PR 작성자 본인** | 승인 + 검사 통과 후 Squash and merge | [02](docs/02-submit-solution.md) |

## 핵심 규칙 10가지

1. `main` 에 직접 푸시하지 않습니다. **항상 브랜치 → PR** 입니다.
2. 브랜치 이름: `solve/<github-id>/<플랫폼>-<id>`, `problem/<플랫폼>-<id>`, `docs/<주제>`
3. 문제 폴더: `problems/<플랫폼>/<id>-<영문-slug>/` (소문자, 숫자, 하이픈만)
4. **풀이는 파이썬만** 받습니다. 파일: `solutions/<github-id>.py`, 같은 문제의 두 번째 풀이는 `<github-id>_<설명>.py`
5. 풀이 파일 맨 위에는 템플릿 헤더(결과, 복잡도, 접근)를 채웁니다.
6. **문제 원문은 복사하지 않습니다.** 링크 + 직접 쓴 요약만.
7. 전체 목록 [`PROBLEMS.md`](https://github.com/Hoesu/scsa-archive/blob/index/PROBLEMS.md)는 머지되면 `index` 브랜치에 자동으로 갱신됩니다. 직접 만들거나 올리지 않습니다.
8. **PR 1개 = 문제 1개.** 여러 문제를 한 PR에 섞지 않습니다. (리뷰하기 어려워요)
9. PR 은 **1명 이상 승인 + 자동 검사 통과** 후 작성자가 직접 머지합니다.
10. **기브 앤 테이크**: PR 을 1개 올렸다면 다른 사람 PR 도 1개 리뷰해 주세요.

## 커밋 메시지

```
<타입>: <요약>

solve:   풀이 추가/수정       예) solve: swea 1206 View
problem: 문제 등록/수정       예) problem: codetree maze-escape 등록
docs:    문서                 예) docs: 리뷰 가이드에 예시 추가
chore:   스크립트, 설정 등     예) chore: validate.py 에 경고 추가
```

## 로컬에서 쓰는 스크립트

모두 Python 3.9+ 표준 라이브러리만 사용하므로 별도 설치가 필요 없습니다.

| 명령 | 하는 일 |
|---|---|
| `python scripts/new_problem.py` | 새 문제 폴더 생성 (대화형) |
| `python scripts/new_solution.py <문제경로> --author <id>` | 내 풀이 파일 생성 |
| `python scripts/validate.py` | 구조·이름 규칙 검사 (PR 올리기 전에!) |
| `python scripts/build_index.py` | PROBLEMS.md 미리 보기 (로컬 전용, 자동으로 커밋 제외됨) |

> Windows 에서 `python` 이 안 되면 `py` 로 바꿔서 실행해 보세요.

## 행동 강령

- 리뷰는 **사람이 아니라 코드**에 대해 합니다.
- "왜 이렇게 짰어요?" 대신 "이 부분은 어떤 의도인지 궁금해요!" 처럼 말해 주세요.
- 질문에는 정답이 없습니다. 어떤 질문도 환영합니다.
- 다른 사람의 풀이를 자기 이름으로 올리지 않습니다. 참고했다면 헤더에 출처를 적어주세요.
