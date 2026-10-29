# SCSA Archive

> 반 전체가 함께 만드는 **코딩테스트 문제 은행**
> Codetree · SWEA · Programmers · 백준 · 정올에서 좋은 문제를 발굴하고, **파이썬으로** 함께 풀고, 서로의 코드를 리뷰합니다.

- **문제 은행 구축**: 시험 대비에 실제로 도움이 되는 문제를 유형별·난이도별로 모읍니다.
- **GitHub 협업 연습**: Issue → Pull Request → Code Review → Merge 흐름을 직접 경험합니다.

**📋 [전체 문제 목록](https://github.com/Hoesu/scsa-archive/blob/index/PROBLEMS.md)** · **💡 [문제 제안하기](https://github.com/Hoesu/scsa-archive/issues/new/choose)** · **🙋 [질문·토론](https://github.com/Hoesu/scsa-archive/discussions)**

---

## 3분 시작하기

이 저장소에서 하는 일은 크게 두 가지입니다. **좋은 문제를 제안**하고, **문제를 풀어 풀이를 올리는 것**.

### 준비 (처음 한 번만)

```bash
git clone https://github.com/Hoesu/scsa-archive.git
cd scsa-archive
```

> [!TIP]
> Git·Python 설치나 GitHub 초대 수락이 아직이라면 [00. 환경 준비](docs/00-getting-started.md) 를 먼저 보세요.

### A. 문제 제안하기

**1) 이슈로 제안** — GitHub 웹에서만 하면 됩니다.

**Issues → New issue → 문제 제안** 을 고르고 칸을 채운 뒤 **Submit** 하세요.
반 친구들이 👍 로 투표하고, 운영진이 `채택` 라벨을 붙여줍니다.

**2) 채택되면 등록** — 이슈 번호 하나로 문제 폴더가 만들어집니다.

```bash
git switch main && git pull
git switch -c problem/<플랫폼>-<번호>              # 예) problem/programmers-12906
python scripts/new_problem.py --issue <이슈 번호>   # 이슈에 적은 정보를 그대로 가져옵니다
```

만들어진 README 에 **문제 요약과 힌트**를 쓰고, 스크립트가 알려주는 명령으로 커밋 → 푸시 → PR 을 올리면 끝입니다.

### B. 풀이 올리기

**1) 풀이 파일 만들기** — 문제 이름 **일부만** 넣으면 됩니다.

```bash
git switch main && git pull
python scripts/new_solution.py 같은숫자
```

문제 검색, 작업 브랜치 생성, 풀이 파일 생성을 스크립트가 알아서 합니다. (처음 한 번만 GitHub ID 를 물어봐요)

**2) 코드 작성** — 만들어진 `solutions/<내아이디>.py` 의 맨 위 헤더(결과, 접근)를 채우고 코드를 작성합니다.

**3) 올리기** — 스크립트가 마지막에 출력한 명령을 그대로 실행합니다.

```bash
python scripts/validate.py
git add problems/
git commit -m "[풀이] 같은 숫자는 싫어"
git push -u origin solve/<내아이디>/programmers-12906
```

**4) PR** — GitHub 의 **Compare & pull request** 를 누르고, 리뷰 승인 1개를 받으면 **Squash and merge** 합니다.

> [!TIP]
> 뭘 풀지 고민된다면 [전체 문제 목록](https://github.com/Hoesu/scsa-archive/blob/index/PROBLEMS.md) 맨 위의 **풀이를 기다리는 문제** 부터!

---

## 문서 안내

| 이럴 때 | 문서 |
|---|---|
| 처음이라 무엇부터 할지 모르겠어요 | [CONTRIBUTING.md](CONTRIBUTING.md) — 전체 흐름과 규칙 요약 |
| Git·Python 설치, 초대 수락 | [00. 환경 준비](docs/00-getting-started.md) |
| 좋은 문제를 발견했어요 | [01. 문제 제안·등록](docs/01-propose-problem.md) |
| 문제를 풀었어요 | [02. 풀이 제출](docs/02-submit-solution.md) |
| 다른 사람 코드에 의견을 주고 싶어요 | [03. 코드 리뷰](docs/03-code-review.md) |
| 폴더 이름, 난이도, 태그 규칙이 궁금해요 | [04. 폴더 구조와 네이밍](docs/04-directory-structure.md) |
| 질문은 어디에? GitHub 기능을 더 써보고 싶어요 | [05. GitHub 기능 둘러보기](docs/05-github-features.md) |
| Git 명령이 헷갈려요, 실수했어요 | [06. Git 치트시트](docs/06-git-cheatsheet.md) |
| (운영진) 저장소 설정 | [관리자 설정](docs/admin-setup.md) |

## 꼭 지켜주세요

- **문제 원문을 복사하지 않습니다.** 링크와 직접 쓴 요약만 올립니다. (플랫폼 저작권 보호)
- **풀이는 파이썬(`.py`)만** 받습니다.
- **스스로 풀기 전에는 `solutions/` 를 열지 않기**를 권장합니다. 힌트는 문제 README 의 접힌 블록에 있어요.
- 리뷰는 **코드에 대해서만**, 친절하게. 모두 배우는 중입니다.

## 저장소 구조

```
scsa-archive/
├── problems/                       문제 은행 본체
│   └── <플랫폼>/<문제id>-<slug>/    예) programmers/12906-same-numbers
│       ├── README.md               문제 정보 + 요약 + 힌트
│       └── solutions/
│           └── <GitHub ID>.py      사람마다 한 파일
├── scripts/                        문제·풀이 생성, 검사 스크립트
├── templates/                      문제 README, 풀이 템플릿
├── docs/                           사용 설명서
└── .github/                        이슈·PR 템플릿, 자동화(Actions)
```

전체 문제 목록(`PROBLEMS.md`)은 머지될 때마다 `index` 브랜치에 자동으로 만들어집니다.
구조를 이렇게 정한 이유는 [04. 폴더 구조와 네이밍](docs/04-directory-structure.md) 에 있습니다.
