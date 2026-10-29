# 관리자 설정 (최초 1회)

저장소 소유자/운영진이 반 전체를 초대하기 전에 해야 하는 설정입니다.
GitHub 화면 이름은 2026년 기준이며, 메뉴 위치는 조금씩 바뀔 수 있습니다.

## 체크리스트

- [ ] 1. 코드 푸시 (이 템플릿 파일들)
- [ ] 2. 라벨 생성
- [ ] 3. 기본 기능 켜기 (Discussions, Projects)
- [ ] 4. PR 머지 방식 설정
- [ ] 5. `main` 브랜치 보호
- [ ] 6. Actions 권한 확인
- [ ] 7. 팀원 초대
- [ ] 8. 첫 주 Milestone / Projects 보드 / Discussions 고정 글 만들기

## 1. 코드 푸시

```bash
git add .
git commit -m "chore: 문제 은행 초기 구조 세팅"
git push origin main
```

> 브랜치 보호(5번)를 켜기 **전에** 푸시해야 합니다.

## 2. 라벨 생성

[GitHub CLI](https://cli.github.com) 설치 후:

```bash
gh auth login
python scripts/setup_labels.py
```

라벨 목록은 `scripts/setup_labels.py` 에 있습니다. 이슈 템플릿과 `.github/labeler.yml` 이 이 이름들을 사용하므로, 이름을 바꿀 때는 세 파일을 함께 수정하세요.
GitHub 기본 라벨(`bug`, `enhancement` 등)은 **Issues → Labels** 에서 지워도 됩니다.

## 3. 기본 기능 켜기

**Settings → General → Features**

- [x] Issues
- [x] Discussions → 켠 뒤 카테고리 정리 (예: 📣 공지, 🙋 Q&A, 💬 자유, 📝 주간 회고, 👋 자기소개)
- [x] Projects
- [ ] Wiki (docs/ 폴더를 쓰므로 꺼도 됨)

## 4. PR 머지 방식

**Settings → General → Pull Requests**

- [x] Allow squash merging → Default commit message: **Pull request title**
- [ ] Allow merge commits (끔)
- [ ] Allow rebase merging (끔)
- [x] Always suggest updating pull request branches
- [x] Automatically delete head branches

squash 하나만 허용하면 `main` 기록이 "PR 1개 = 커밋 1개" 로 깔끔하게 유지됩니다.

## 5. main 브랜치 보호

**Settings → Rules → Rulesets → New ruleset → New branch ruleset**

| 항목 | 값 |
|---|---|
| Ruleset name | `protect-main` |
| Enforcement status | Active |
| Target branches | Include default branch |
| Restrict deletions | ✅ |
| Block force pushes | ✅ |
| Require a pull request before merging | ✅ |
| └ Required approvals | `1` |
| └ Dismiss stale pull request approvals when new commits are pushed | 선택 (켜면 엄격, 끄면 편함) |
| └ Require conversation resolution before merging | ✅ (리뷰 코멘트를 무시하고 머지하는 것 방지) |
| Require status checks to pass | ✅ → `validate` 추가 (PR 을 한 번 올려서 검사가 실행된 뒤에 목록에 나타남) |

### 자동 커밋 허용 (중요)

`build-index` 워크플로는 머지 후 `PROBLEMS.md` 를 `main` 에 **직접 커밋**합니다.
위 규칙이 이 커밋까지 막으면 워크플로가 실패하므로, 다음 중 하나를 선택하세요.

- **방법 A (권장)**: Ruleset 의 **Bypass list → Add bypass** 에서 GitHub Actions 앱을 추가
  (목록에 보이지 않으면 방법 B)
- **방법 B**: Personal Access Token(fine-grained, 이 저장소 `Contents: Read and write`)을 만들어
  **Settings → Secrets and variables → Actions** 에 `INDEX_TOKEN` 으로 저장하고,
  `build-index.yml` 의 checkout 단계에 `with: token: ${{ secrets.INDEX_TOKEN }}` 를 추가 (토큰 소유자가 bypass 권한을 가진 관리자여야 함)
- **방법 C**: 자동 갱신을 포기하고 운영진이 주기적으로 `python scripts/build_index.py` 후 PR 로 반영

## 6. Actions 권한

**Settings → Actions → General**

- Actions permissions: **Allow all actions and reusable workflows** (또는 GitHub/verified creator 만 허용)
- Workflow permissions: 각 워크플로 파일에 필요한 권한을 명시해 두었으므로 기본값(**Read repository contents**)으로 둬도 됩니다.
- Fork 에서 온 PR 의 워크플로 실행 승인: "Require approval for first-time contributors" 권장

## 7. 팀원 초대

**Settings → Collaborators → Add people** 에서 GitHub ID 로 초대합니다. 권한은 **Write**.

- 인원이 많으면 GitHub Organization 을 만들고 **Team** 단위로 권한을 주는 것이 관리하기 편합니다.
  (Organization 으로 옮기면 저장소 URL 이 바뀌니, 문서 안의 `Hoesu/scsa-archive` 링크를 일괄 수정하세요)
- 운영진이 여러 명이면 `.github/CODEOWNERS` 를 만들어 `docs/`, `scripts/`, `.github/` 변경 시 운영진 리뷰를 자동 요청하게 할 수 있습니다.

```
# .github/CODEOWNERS 예시
/scripts/   @Hoesu
/.github/   @Hoesu
/docs/      @Hoesu
```

## 8. 운영 준비

- **Milestone**: Issues → Milestones → New milestone → `Week 01 (MM/DD ~ MM/DD)`, 마감일 설정
- **Projects**: 저장소 Projects 탭 → New project → Board → 컬럼: `제안됨`, `이번 주 문제`, `등록 완료`, `이번 주 종료`
  → Workflows 설정에서 "Item added → 제안됨", "Item closed → 등록 완료" 자동화를 켜면 편합니다.
- **Discussions 고정 글**: 공지(운영 규칙 요약 + CONTRIBUTING 링크), 자기소개 스레드, 주간 회고 스레드

## 주간 운영 루틴 (예시)

| 요일 | 할 일 |
|---|---|
| 월 | 지난주 `채택` 이슈 중 3~5개를 이번 주 Milestone 에 배정, 공지 |
| 화~목 | 문제 등록/풀이 PR 리뷰. 오래 방치된 PR 에 리뷰어 지정 |
| 금 | 주간 회고 스레드 열기, Milestone 닫기, PROBLEMS.md 기여 현황 공유 |
