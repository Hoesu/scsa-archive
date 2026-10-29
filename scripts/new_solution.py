"""문제 폴더에 내 풀이 파일을 템플릿으로 만든다.

사용법:
    python scripts/new_solution.py problems/programmers/12906-same-numbers --author hoesu
    python scripts/new_solution.py problems/swea/1206-view --author hoesu --variant stack

--variant 를 주면 hoesu_stack.py 처럼 같은 사람이 여러 풀이를 올릴 수 있다.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import (
    PLATFORMS,
    ROOT,
    SOLUTION_EXT,
    SOLUTION_FILE_RE,
    TEMPLATES_DIR,
    parse_front_matter,
    render_template,
    setup_console,
)


def main() -> int:
    setup_console()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("problem", help="문제 폴더 경로 (예: problems/programmers/12906-same-numbers)")
    p.add_argument("--author", required=True, help="내 GitHub ID")
    p.add_argument("--variant", help="같은 문제에 두 번째 풀이를 올릴 때 구분자 (예: dp, bfs)")
    a = p.parse_args()

    problem_dir = Path(a.problem)
    if not problem_dir.is_absolute():
        problem_dir = (Path.cwd() / problem_dir).resolve()
    readme = problem_dir / "README.md"
    if not readme.is_file():
        p.error(f"문제 폴더가 아니거나 README.md 가 없습니다: {a.problem}")
    meta = parse_front_matter(readme.read_text(encoding="utf-8"))

    name = a.author + (f"_{a.variant}" if a.variant else "") + SOLUTION_EXT
    if not SOLUTION_FILE_RE.match(name):
        p.error(f"파일명 규칙에 맞지 않습니다: {name} (variant 는 소문자/숫자/하이픈)")

    target = problem_dir / "solutions" / name
    if target.exists():
        p.error(f"이미 존재합니다: {target.relative_to(ROOT).as_posix()} (다른 풀이라면 --variant 를 지정하세요)")

    content = render_template(TEMPLATES_DIR / f"solution{SOLUTION_EXT}", {
        "title": meta.get("title", ""),
        "platform": PLATFORMS.get(meta.get("platform", ""), meta.get("platform", "")),
        "id": meta.get("id", ""),
        "url": meta.get("url", ""),
        "author": a.author,
    })
    target.parent.mkdir(exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    gitkeep = target.parent / ".gitkeep"
    if gitkeep.exists():
        gitkeep.unlink()

    print(f"생성 완료: {target.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
