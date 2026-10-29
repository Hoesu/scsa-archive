# 06. Git 치트시트

## 기본 흐름

```bash
git switch main && git pull                           # 1. 최신화
git switch -c solve/<id>/programmers-12906            # 2. 브랜치 생성
# ... 작업 ...
git status                                            # 3. 변경 확인
git add <파일>                                         # 4. 스테이징
git commit -m "[풀이] 같은 숫자는 싫어"                # 5. 커밋
git push -u origin solve/<id>/programmers-12906       # 6. 푸시 (처음엔 -u)
# 7. GitHub 에서 PR 생성 → 리뷰 → 머지
git switch main && git pull && git branch -d solve/<id>/programmers-12906   # 8. 정리
```

## 자주 쓰는 명령

| 하고 싶은 것 | 명령 |
|---|---|
| 현재 상태 보기 | `git status` |
| 무엇을 바꿨는지 보기 | `git diff` (스테이징 전) / `git diff --staged` (스테이징 후) |
| 커밋 기록 보기 | `git log --oneline --graph -15` |
| 브랜치 목록 | `git branch` (로컬) / `git branch -a` (원격 포함) |
| 브랜치 이동 | `git switch <브랜치>` |
| 다른 사람 PR 브랜치 받아보기 | `git fetch && git switch <브랜치명>` |
| 원격에서 지워진 브랜치 정리 | `git fetch --prune` |

## main 최신 내용을 내 브랜치에 반영하기

PR 을 올려 둔 사이 `main` 이 바뀌어서 충돌이 나거나 최신 내용이 필요할 때:

```bash
git switch main
git pull
git switch solve/<id>/programmers-12906
git merge main          # 충돌이 나면 아래 "충돌 해결" 참고
git push
```

> GitHub PR 화면의 **Update branch** 버튼으로도 같은 일을 할 수 있어요.

## 충돌 (conflict) 해결하기

같은 파일의 같은 부분을 두 사람이 다르게 고치면 Git 이 자동으로 합치지 못합니다.

```
<<<<<<< HEAD
내 브랜치의 내용
=======
main 의 내용
>>>>>>> main
```

1. `git status` 로 충돌 파일 확인 (`both modified`)
2. 파일을 열어 `<<<<<<<`, `=======`, `>>>>>>>` 표시를 지우고 **최종적으로 남길 내용**만 남기기
   (VS Code 는 **Accept Current / Incoming / Both** 버튼을 제공합니다)
3. `git add <파일>` → `git commit` → `git push`

> 이 저장소에서는 풀이 파일이 사람마다 달라서 충돌이 드뭅니다.
> 충돌이 났다면 대부분 **남의 파일이나 같은 문제 README 를 동시에 수정**한 경우입니다.

## 실수 되돌리기

### 커밋 메시지를 잘못 썼어요 (아직 push 전)
```bash
git commit --amend -m "새 메시지"
```

### 파일 하나를 빠뜨리고 커밋했어요 (아직 push 전)
```bash
git add 빠뜨린파일
git commit --amend --no-edit
```

### 수정한 파일을 원래대로 돌리고 싶어요 (커밋 전)
```bash
git restore <파일>             # 작업 내용이 사라지니 주의!
git restore --staged <파일>    # add 만 취소 (내용은 유지)
```

### 실수로 main 에 커밋했어요
아직 push 하지 않았다면, 커밋을 새 브랜치로 옮기고 main 은 원격 상태로 되돌립니다.
```bash
git switch -c solve/<id>/programmers-12906   # 지금 커밋을 가진 채로 새 브랜치 생성
git switch main
git reset --hard origin/main                  # main 을 원격과 같게 (새 브랜치에 커밋이 있으니 안전)
git switch solve/<id>/programmers-12906
```
(`main` 은 보호되어 있어서 push 는 거부됩니다. 걱정 마세요.)

### 이미 push 한 커밋을 취소하고 싶어요
기록을 지우지 말고 **되돌리는 커밋**을 새로 만듭니다.
```bash
git revert <커밋해시>
git push
```

### 아무것도 모르겠어요
```bash
git status        # Git 이 다음에 뭘 해야 하는지 대부분 알려줍니다
git stash         # 지금 작업을 잠시 치워두기 (git stash pop 으로 복구)
```
그래도 모르겠으면 **Discussions 에 `git status` 결과를 붙여서** 질문하세요!

## 용어 정리

| 용어 | 뜻 |
|---|---|
| repository (repo) | 저장소. 파일과 그 모든 변경 기록 |
| clone | 원격 저장소를 내 컴퓨터로 복사 |
| commit | 변경 사항의 스냅샷 + 메시지 |
| branch | 독립적인 작업 공간 (기본 브랜치: `main`) |
| push / pull | 내 커밋 올리기 / 원격 커밋 받기 |
| fetch | 원격 정보만 받아오고 내 브랜치에는 합치지 않음 |
| merge | 두 브랜치를 합치기 |
| PR (Pull Request) | "내 브랜치를 main 에 합쳐 주세요" 라는 요청 + 리뷰 공간 |
| squash merge | PR 의 여러 커밋을 하나로 합쳐서 머지 |
| fork | 남의 저장소를 내 계정으로 복사 |
| upstream / origin | 원본 저장소 / 내가 clone 한 저장소 |
