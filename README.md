# SCSA Archive

> 반 전체가 함께 만드는 **코딩테스트 문제 은행**
> Codetree · SWEA · Programmers · 백준 · 정올 등에서 좋은 문제를 발굴하고, **파이썬으로** 함께 풀고, 서로의 코드를 리뷰합니다.

이 저장소의 목표는 두 가지입니다.

1. **문제 은행 구축**: 시험 대비에 실제로 도움이 되는 문제를 유형별·난이도별로 모아 둡니다.
2. **GitHub 협업 연습**: Issue → Branch → Pull Request → Code Review → Merge 로 이어지는 실무 흐름을 직접 경험합니다.

📋 **[전체 문제 목록 보기 → PROBLEMS.md](PROBLEMS.md)**

---

## 3분 시작하기

예시 문제 **programmers 12906 「같은 숫자는 싫어」** 에 내 풀이를 올려 봅시다.

```
브랜치 만들기  →  풀이 작성  →  검사 · 커밋 · 푸시  →  PR 열기  →  리뷰 · 머지
```

> 명령어의 `<내아이디>` 는 **본인 GitHub ID** 로 바꿔서 입력하세요. (예: `Hoesu`)
> Git 이 처음이라면 [00. 환경 준비](docs/00-getting-started.md) 를 먼저 끝내고 오세요.

### 0단계. 저장소 내려받기 (처음 한 번만)

```bash
git clone https://github.com/Hoesu/scsa-archive.git
cd scsa-archive
```

### 1단계. 작업용 브랜치 만들기

`main` 을 최신으로 받은 뒤, 이 문제 전용 브랜치를 만듭니다.

```bash
git switch main
git pull
git switch -c solve/<내아이디>/programmers-12906
```

### 2단계. 풀이 파일 만들고 코드 작성하기

```bash
python scripts/new_solution.py problems/programmers/12906-same-numbers --author <내아이디>
```

`solutions/<내아이디>.py` 파일이 생깁니다.
맨 위 헤더(결과, 복잡도, 접근)를 채우고, 그 아래에 코드를 작성하세요.

### 3단계. 검사 → 커밋 → 푸시

```bash
python scripts/validate.py          # "에러 0개" 가 나오는지 확인
git add problems/
git commit -m "solve: programmers 12906 같은 숫자는 싫어"
git push -u origin solve/<내아이디>/programmers-12906
```

### 4단계. PR 열고 리뷰 받기

1. GitHub 저장소 페이지에 뜨는 **Compare & pull request** 버튼 클릭
2. PR 템플릿을 채우고 **Create pull request**
3. 리뷰 승인 1개 + 자동 검사 통과 → 본인이 **Squash and merge**

더 자세한 설명은 [02. 풀이 제출](docs/02-submit-solution.md), 전체 규칙은 [CONTRIBUTING.md](CONTRIBUTING.md) 에 있습니다.

## 무엇을 할 수 있나요?

| 하고 싶은 일 | 사용하는 GitHub 기능 | 가이드 |
|---|---|---|
| 좋은 문제를 발견했어요 | **Issue** (문제 제안 템플릿) | [문제 제안·등록](docs/01-propose-problem.md) |
| 문제를 풀었어요 | **Branch + Pull Request** | [풀이 제출](docs/02-submit-solution.md) |
| 다른 사람 코드에 의견을 주고 싶어요 | **Code Review**, Suggested changes | [코드 리뷰](docs/03-code-review.md) |
| 막혀서 질문하고 싶어요 | **Issue** (질문 템플릿) / **Discussions** | [GitHub 기능 둘러보기](docs/05-github-features.md) |
| 이번 주에 뭘 풀지 알고 싶어요 | **Milestones**, **Projects** | [GitHub 기능 둘러보기](docs/05-github-features.md) |

## 저장소 구조

```
scsa-archive/
├── problems/                     # 문제 은행 본체
│   ├── programmers/
│   │   └── 12906-same-numbers/   # <문제id>-<영문slug>
│   │       ├── README.md         # 메타데이터 + 문제 요약 + 힌트
│   │       └── solutions/
│   │           ├── Hoesu.py      # <GitHub ID>.py
│   │           └── Hoesu_dp.py   # 두 번째 풀이는 <ID>_<설명>.py
│   └── swea/  codetree/  boj/  jungol/  leetcode/  etc/
├── PROBLEMS.md                   # 전체 목록 (자동 생성, 직접 수정 금지)
├── templates/                    # 문제 README / 풀이 템플릿
├── scripts/                      # 생성·검사·목록화 스크립트 (Python 표준 라이브러리만 사용)
├── docs/                         # 사용 설명서
└── .github/                      # 이슈/PR 템플릿, 자동화(Actions)
```

구조를 이렇게 정한 이유와 상세 규칙은 [폴더 구조와 네이밍 규칙](docs/04-directory-structure.md)에 있습니다.

## 문서

| 문서 | 내용 |
|---|---|
| [CONTRIBUTING.md](CONTRIBUTING.md) | 기여 규칙 요약 (처음이라면 여기부터) |
| [00. 환경 준비](docs/00-getting-started.md) | Git 설치, 초대 수락, clone, 기본 설정 |
| [01. 문제 제안·등록](docs/01-propose-problem.md) | Issue 로 제안하고 PR 로 등록하기 |
| [02. 풀이 제출](docs/02-submit-solution.md) | 브랜치 → 커밋 → PR → 머지 |
| [03. 코드 리뷰](docs/03-code-review.md) | 좋은 리뷰 작성법, 리뷰 코멘트 규칙 |
| [04. 폴더 구조와 네이밍](docs/04-directory-structure.md) | 플랫폼별 문제 정리 규칙, 난이도 기준표 |
| [05. GitHub 기능 둘러보기](docs/05-github-features.md) | Issue, Label, Milestone, Projects, Discussions, Actions 실습 미션 |
| [06. Git 치트시트](docs/06-git-cheatsheet.md) | 자주 쓰는 명령, 충돌 해결, 실수 되돌리기 |
| [관리자 설정](docs/admin-setup.md) | 저장소 관리자가 최초 1회 해야 하는 설정 |

## 꼭 지켜주세요

- **문제 원문을 복사하지 않습니다.** 링크와 직접 쓴 요약만 올립니다. (각 플랫폼의 저작권 보호)
- **스스로 풀기 전에는 `solutions/` 를 열지 않는 것**을 권장합니다. 힌트는 README 의 접힌 블록에 있어요.
- 리뷰는 **코드에 대해서만**, 친절하게. 모두 배우는 중입니다.
