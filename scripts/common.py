"""스크립트들이 공유하는 상수와 유틸리티.

외부 패키지 없이 표준 라이브러리만 사용한다. (누구나 바로 실행할 수 있도록)
"""

from __future__ import annotations

import os
import re
import sys
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

# 문제 폴더: 소문자/숫자와 하이픈만 (예: 12906-same-numbers, maze-escape)
PROBLEM_DIR_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# 풀이 파일: <github-id>[_<설명>].py (예: hoesu.py, hoesu_bfs.py)
SOLUTION_FILE_RE = re.compile(r"^(?P<author>[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)(?:_(?P<variant>[a-z0-9-]+))?(?P<ext>\.[a-z]+)$")


def setup_console() -> None:
    """Windows 콘솔에서도 한글 출력이 깨지지 않도록 UTF-8로 맞춘다."""
    for stream in (sys.stdout, sys.stderr):
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


def render_template(path: Path, values: dict) -> str:
    text = path.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text
