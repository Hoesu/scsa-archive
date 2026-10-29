# 00. 환경 준비

처음 한 번만 하면 됩니다. 15분 정도 걸려요.

## 1. 준비물

| 도구 | 확인 명령 | 설치 |
|---|---|---|
| Git | `git --version` | https://git-scm.com (Windows 는 Git for Windows, 설치 옵션은 기본값) |
| Python 3.9+ | `python --version` (또는 `py --version`) | https://www.python.org (설치 시 **Add python.exe to PATH** 체크) |
| GitHub 계정 | - | https://github.com |
| (선택) VS Code | - | Git 연동과 마크다운 미리보기가 편해요 |

## 2. 저장소 초대 수락

관리자가 Collaborator 로 초대하면 GitHub 에 가입한 이메일로 초대 메일이 옵니다.
메일의 **View invitation → Accept invitation** 을 누르세요.
(메일이 안 보이면 https://github.com/Hoesu/scsa-archive/invitations 로 직접 접속)

> 초대를 받지 못했다면 **Fork** 방식으로도 참여할 수 있습니다. 아래 [Fork 로 참여하기](#fork-로-참여하기)를 보세요.

## 3. Git 최초 설정

커밋에 남을 이름과 이메일입니다. **GitHub 계정 이메일**과 같게 해야 잔디(기여 그래프)가 심어집니다.

```bash
git config --global user.name "홍길동"
git config --global user.email "my-github-email@example.com"
git config --global init.defaultBranch main
git config --global core.autocrlf true      # Windows 만 (macOS/Linux 는 input)
git config --global core.quotepath false     # 한글 파일명이 깨져 보이지 않도록
```

## 4. 저장소 내려받기 (clone)

```bash
cd ~/Desktop
git clone https://github.com/Hoesu/scsa-archive.git
cd scsa-archive
python scripts/validate.py     # "에러 0개" 가 나오면 준비 완료!
```

처음 `git push` 를 할 때 GitHub 로그인 창이 뜹니다. 브라우저로 로그인하면 이후에는 자동입니다.

## 5. 매일 작업 시작 전 루틴

```bash
git switch main
git pull                      # 다른 사람들이 머지한 최신 내용 받기
git switch -c solve/<내아이디>/<플랫폼>-<번호>   # 새 작업은 새 브랜치에서
```

## Fork 로 참여하기

Collaborator 가 아니어도 참여할 수 있습니다. 오픈소스에 기여하는 방식과 같아요.

1. 저장소 우측 상단 **Fork** 클릭 → 내 계정에 복사본 생성
2. 내 복사본을 clone: `git clone https://github.com/<내아이디>/scsa-archive.git`
3. 원본을 `upstream` 으로 등록: `git remote add upstream https://github.com/Hoesu/scsa-archive.git`
4. 최신화할 때: `git switch main && git pull upstream main && git push`
5. 브랜치에서 작업 → 내 Fork 에 push → GitHub 에서 **원본 저장소로 PR**

나머지 흐름(리뷰, 머지)은 동일합니다. 단, 머지 버튼은 Collaborator 만 누를 수 있으니 승인 후 운영진에게 머지를 요청하세요.

---

다음: [01. 문제 제안·등록](01-propose-problem.md)
