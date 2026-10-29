"""문제 은행의 폴더 구조와 메타데이터 규칙을 검사한다.

사용법:
    python scripts/validate.py
    python scripts/validate.py --author <github-id> --base origin/main   # PR 검사용 (CI)

에러가 하나라도 있으면 종료 코드 1을 반환한다.
경고(warning)는 머지를 막지 않지만 리뷰 때 확인해 주세요.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from common import (
    PLATFORMS,
    PROBLEM_DIR_RE,
    PROBLEM_ID_RE,
    PROBLEMS_DIR,
    REQUIRED_KEYS,
    ROOT,
    SOLUTION_EXT,
    SOLUTION_FILE_RE,
    git,
    iter_problem_dirs,
    iter_solution_files,
    nfc,
    parse_front_matter,
    setup_console,
)

IN_CI = os.environ.get("GITHUB_ACTIONS") == "true"


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def _emit(self, level: str, path: Path, msg: str) -> str:
        rel = path.relative_to(ROOT).as_posix()
        if IN_CI:
            # GitHub Actions 주석 형식 -> PR의 Files changed 탭에 바로 표시된다
            print(f"::{level} file={rel}::{msg}")
        return f"{rel}: {msg}"

    def error(self, path: Path, msg: str) -> None:
        self.errors.append(self._emit("error", path, msg))

    def warn(self, path: Path, msg: str) -> None:
        self.warnings.append(self._emit("warning", path, msg))


def check_problem(problem_dir: Path, report: Report, seen_ids: dict) -> None:
    platform = problem_dir.parent.name
    name = nfc(problem_dir.name)
    if not PROBLEM_DIR_RE.match(name):
        report.error(problem_dir, "폴더명은 한글/영문 소문자/숫자와 하이픈만 사용합니다 (예: 12906-같은-숫자는-싫어)")

    readme = problem_dir / "README.md"
    if not readme.is_file():
        report.error(problem_dir, "README.md 가 없습니다")
        return

    try:
        meta = parse_front_matter(readme.read_text(encoding="utf-8"))
    except ValueError as e:
        report.error(readme, str(e))
        return

    missing = [k for k in REQUIRED_KEYS if not meta.get(k)]
    if missing:
        report.error(readme, f"필수 항목 누락: {', '.join(missing)}")

    if meta.get("platform") and meta["platform"] != platform:
        report.error(readme, f"platform 값({meta['platform']})이 상위 폴더명({platform})과 다릅니다")

    pid = str(meta.get("id", ""))
    if pid and not PROBLEM_ID_RE.match(pid):
        report.error(readme, f"id 는 영문 소문자/숫자와 하이픈(-)만 사용합니다: {pid} (예: 12906, baby-whale-first-voyage)")
    if pid.isdigit() and not (name == pid or name.startswith(pid + "-")):
        report.error(readme, f"번호가 있는 문제는 폴더명이 번호로 시작해야 합니다 (예: {pid}-문제-제목)")
    if pid:
        other = seen_ids.setdefault((platform, pid.lower()), problem_dir)
        if other != problem_dir:
            report.error(readme, f"같은 id({pid})의 문제가 이미 있습니다: {other.relative_to(ROOT).as_posix()}")

    if meta.get("url") and not str(meta["url"]).startswith(("http://", "https://")):
        report.error(readme, "url 은 http(s):// 로 시작해야 합니다")

    if meta.get("difficulty") and meta["difficulty"] not in {"1", "2", "3", "4", "5"}:
        report.error(readme, "difficulty 는 1~5 사이 정수입니다 (docs/04-directory-structure.md 참고)")

    if "tags" in meta and not isinstance(meta["tags"], list):
        report.error(readme, "tags 는 [태그1, 태그2] 형식의 리스트여야 합니다")

    allowed = {"README.md", "solutions"}
    for child in problem_dir.iterdir():
        if child.name not in allowed:
            report.warn(child, "문제 폴더에는 README.md 와 solutions/ 만 두는 것을 권장합니다")

    for f in iter_solution_files(problem_dir):
        m = SOLUTION_FILE_RE.match(f.name)
        if not m:
            report.error(f, "풀이 파일명은 <github-id>.py 또는 <github-id>_<설명>.py 형식입니다")
        elif m["ext"] != SOLUTION_EXT:
            report.error(f, f"파이썬(.py) 풀이만 받습니다: {m['ext']} 파일은 올릴 수 없어요")


def check_tree(report: Report) -> None:
    if not PROBLEMS_DIR.is_dir():
        return
    for child in PROBLEMS_DIR.iterdir():
        if child.is_dir() and child.name not in PLATFORMS:
            report.error(child, f"알 수 없는 플랫폼 폴더입니다 (허용: {', '.join(PLATFORMS)})")
        elif child.is_file() and child.name != ".gitkeep":
            report.warn(child, "problems/ 바로 아래에는 플랫폼 폴더만 둡니다")
    seen_ids: dict = {}
    for problem_dir in iter_problem_dirs():
        if problem_dir.parent.name in PLATFORMS:
            check_problem(problem_dir, report, seen_ids)


def check_authorship(author: str, base: str, report: Report) -> None:
    """PR에서 새로 추가된 풀이 파일명이 PR 작성자의 GitHub ID로 시작하는지 확인 (경고만)."""
    r = git("diff", "--name-only", "--diff-filter=A", f"{base}...HEAD")
    if r.returncode != 0:
        print(f"(작성자 검사 건너뜀: {r.stderr.strip()})")
        return
    for rel in r.stdout.splitlines():
        path = ROOT / rel
        if path.parent.name != "solutions" or not rel.startswith("problems/"):
            continue
        m = SOLUTION_FILE_RE.match(path.name)
        if m and m["author"].lower() != author.lower():
            report.warn(path, f"풀이 파일명({m['author']})이 PR 작성자({author})와 다릅니다. 본인 GitHub ID를 사용했는지 확인하세요")


def main() -> int:
    setup_console()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--author", help="PR 작성자 GitHub ID (풀이 파일명 확인용)")
    parser.add_argument("--base", default="origin/main", help="비교 기준 브랜치 (기본: origin/main)")
    args = parser.parse_args()

    report = Report()
    check_tree(report)
    if args.author:
        check_authorship(args.author, args.base, report)

    if not IN_CI:
        for w in report.warnings:
            print(f"[경고] {w}")
        for e in report.errors:
            print(f"[에러] {e}")

    count = sum(1 for _ in iter_problem_dirs())
    print(f"\n검사 완료: 문제 {count}개, 에러 {len(report.errors)}개, 경고 {len(report.warnings)}개")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
