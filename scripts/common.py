"""스크립트들이 공유하는 상수와 유틸리티.

외부 패키지 없이 표준 라이브러리만 사용한다. (누구나 바로 실행할 수 있도록)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"
TEMPLATES_DIR = ROOT / "templates"

# PROBLEMS.md 는 main 이 아닌 index 브랜치에 게시되므로, 문제 링크는 main 을 가리키는 절대 URL 로 만든다
REPO = os.environ.get("GITHUB_REPOSITORY", "Hoesu/scsa-archive")
REPO_URL = "{}/{}".format(os.environ.get("GITHUB_SERVER_URL", "https://github.com"), REPO)
INDEX_URL = f"{REPO_URL}/blob/index/PROBLEMS.md"

# 폴더명(key) -> 표시 이름
PLATFORMS = {
    "codetree": "Codetree",
    "swea": "SW Expert Academy",
    "programmers": "Programmers",
    "boj": "Baekjoon",
    "jungol": "JUNGOL",
    "leetcode": "LeetCode",
    "etc": "기타",
}

# 이 저장소는 파이썬 풀이만 받는다
SOLUTION_EXT = ".py"

DIFFICULTY_LABELS = {
    1: "입문",
    2: "기초",
    3: "중급",
    4: "상급",
    5: "최상급",
}

REQUIRED_KEYS = ("title", "platform", "id", "url", "level", "difficulty", "tags", "proposer")

# 문제 id: 소문자/숫자와 하이픈만 (예: 12906, baby-whale-first-voyage). 브랜치 이름에도 쓰인다
PROBLEM_ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# 문제 폴더: 한글/소문자/숫자와 하이픈만 (예: 12906-같은-숫자는-싫어, 아기-고래의-첫-항해)
PROBLEM_DIR_RE = re.compile(r"^[0-9a-z가-힣]+(-[0-9a-z가-힣]+)*$")
PROBLEM_DIR_MAX = 50
# 풀이 파일: <github-id>[_<설명>].py (예: hoesu.py, hoesu_bfs.py)
SOLUTION_FILE_RE = re.compile(r"^(?P<author>[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)(?:_(?P<variant>[a-z0-9-]+))?(?P<ext>\.[a-z]+)$")


def setup_console() -> None:
    """Windows 콘솔·Git Bash 에서도 한글 입출력이 깨지지 않도록 UTF-8로 맞춘다."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def parse_front_matter(text: str) -> dict:
    """README.md 맨 위의 `---`로 둘러싼 메타데이터를 읽는다.

    지원 문법은 의도적으로 단순하다: `key: value` 와 `key: [a, b, c]` 리스트만 허용.
    """
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("README.md 첫 줄이 '---' 로 시작해야 합니다 (front matter 누락)")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError("front matter를 닫는 '---' 줄이 없습니다") from None

    meta: dict = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"'key: value' 형식이 아닌 줄: {line!r}")
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = (v.strip().strip("\"'") for v in value[1:-1].split(","))
            meta[key.strip()] = [v for v in items if v]
        else:
            meta[key.strip()] = value.strip("\"'")
    return meta


def iter_problem_dirs():
    """problems/<platform>/<problem>/ 디렉터리를 정렬된 순서로 돌려준다."""
    if not PROBLEMS_DIR.is_dir():
        return
    for platform_dir in sorted(p for p in PROBLEMS_DIR.iterdir() if p.is_dir()):
        for problem_dir in sorted(p for p in platform_dir.iterdir() if p.is_dir()):
            yield problem_dir


def iter_solution_files(problem_dir: Path):
    solutions = problem_dir / "solutions"
    if not solutions.is_dir():
        return
    for f in sorted(solutions.iterdir()):
        if f.is_file() and f.name != ".gitkeep":
            yield f


def nfc(s: str) -> str:
    """macOS 는 한글 파일명을 자모 분리(NFD)로 돌려줄 수 있어 완성형(NFC)으로 맞춘다."""
    return unicodedata.normalize("NFC", s)


def problem_dir_name(pid: str, title: str) -> str:
    """문제 폴더 이름: 숫자 id 면 '<id>-<제목>', 아니면 '<제목>'. 제목은 한글/영문/숫자만 남긴다."""
    slug = re.sub(r"[^0-9a-z가-힣]+", "-", nfc(title).lower()).strip("-")
    if len(slug) > PROBLEM_DIR_MAX:
        slug = slug[:PROBLEM_DIR_MAX].rsplit("-", 1)[0]
    if slug.startswith(pid + "-"):  # "1. Two Sum" 처럼 제목에 번호가 들어 있는 경우
        slug = slug[len(pid) + 1:]
    if not pid.isdigit():
        return slug or pid
    return f"{pid}-{slug}" if slug else pid


def git(*args: str, timeout: int = 60) -> subprocess.CompletedProcess:
    """git 명령 실행. 한글 경로가 깨지지 않도록 quotepath 를 끄고 UTF-8 로 읽는다."""
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    try:
        return subprocess.run(
            ["git", "-c", "core.quotepath=false", *args], cwd=ROOT, capture_output=True,
            encoding="utf-8", errors="replace", env=env, timeout=timeout,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return subprocess.CompletedProcess(args, 1, "", str(e))


def current_branch() -> str:
    return git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()


def update_main() -> None:
    """main 브랜치에서 실행했다면 최신 내용을 받아 둔다. 실패해도 작업은 계속한다."""
    if current_branch() != "main":
        return
    print("main 을 최신으로 받는 중...", end=" ", flush=True)
    r = git("pull", "--ff-only")
    if r.returncode == 0:
        print("완료\n")
    else:
        reason = (r.stderr or r.stdout).strip().splitlines()
        print("실패 (이대로 계속합니다)")
        if reason:
            print(f"  {reason[-1]}")
        print("  나중에 직접 받아보세요: git pull\n")


def switch_branch(branch: str) -> bool:
    """branch 로 이동한다 (없으면 새로 만든다). 지금 작업 중인 변경 사항은 그대로 따라간다."""
    exists = git("rev-parse", "--verify", "--quiet", f"refs/heads/{branch}").returncode == 0
    r = git("switch", branch) if exists else git("switch", "-c", branch)
    if r.returncode != 0:
        print(f"  * 브랜치를 자동으로 만들지 못했습니다: {r.stderr.strip()}")
        print(f"    직접 만들어 주세요: git switch -c {branch}")
        return False
    print(f"브랜치 {'이동' if exists else '생성'}: {branch}")
    return True


def render_template(path: Path, values: dict) -> str:
    text = path.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text
