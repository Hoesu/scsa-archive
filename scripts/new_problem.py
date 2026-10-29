"""새 문제 폴더를 템플릿으로 만든다.

사용법 (인자를 생략하면 하나씩 물어본다):
    python scripts/new_problem.py
    python scripts/new_problem.py --platform programmers --id 12906 --slug same-numbers \\
        --title "같은 숫자는 싫어" --url https://school.programmers.co.kr/learn/courses/30/lessons/12906 \\
        --level Lv.1 --difficulty 1 --tags "스택/큐,구현" --proposer hoesu
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date

from common import (
    DIFFICULTY_LABELS,
    PLATFORMS,
    PROBLEM_DIR_RE,
    PROBLEMS_DIR,
    ROOT,
    TEMPLATES_DIR,
    render_template,
    setup_console,
)


def ask(prompt: str, validate=None, default: str | None = None) -> str:
    hint = f" [{default}]" if default else ""
    while True:
        value = input(f"{prompt}{hint}: ").strip() or (default or "")
        error = validate(value) if validate else (None if value else "값을 입력하세요")
        if not error:
            return value
        print(f"  -> {error}")


def v_platform(v):
    return None if v in PLATFORMS else f"다음 중 하나: {', '.join(PLATFORMS)}"


def v_slug(v):
    return None if PROBLEM_DIR_RE.match(v) else "소문자/숫자/하이픈만 사용 (예: same-numbers)"


def v_optional_slug(v):
    return None if not v or PROBLEM_DIR_RE.match(v) else v_slug(v)


def v_difficulty(v):
    return None if v in {"1", "2", "3", "4", "5"} else "1~5 사이 숫자"


def v_url(v):
    return None if v.startswith(("http://", "https://")) else "http(s):// 로 시작해야 합니다"


def main() -> int:
    setup_console()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for name in ("platform", "id", "slug", "title", "url", "level", "difficulty", "tags", "proposer"):
        p.add_argument(f"--{name}")
    a = p.parse_args()

    print("새 문제 등록 (Ctrl+C 로 취소)\n")
    platform = a.platform or ask(f"플랫폼 ({'/'.join(PLATFORMS)})", v_platform)
    if v_platform(platform):
        p.error(v_platform(platform))

    if platform == "codetree":
        print("  * Codetree 는 문제 번호가 없으므로 URL 마지막의 영문 이름을 id 로 씁니다 (예: maze-escape)")
    pid = (a.id or ask("문제 id (번호 또는 영문 slug)", v_slug)).lower()
    if v_slug(pid):
        p.error(f"id: {v_slug(pid)}")

    platform_dir = PROBLEMS_DIR / platform
    existing = [d for d in platform_dir.glob(f"{pid}*") if d.is_dir() and re.match(rf"^{re.escape(pid)}(-|$)", d.name)]
    if existing:
        rel = existing[0].relative_to(ROOT).as_posix()
        print(f"\n이미 등록된 문제입니다: {rel}")
        print(f"풀이만 추가하려면: python scripts/new_solution.py {rel} --author <github-id> --lang py")
        return 1

    if a.slug is not None:
        slug = a.slug
    elif pid.isdigit():
        slug = ask("영문 slug (폴더명용, 예: same-numbers / 생략 가능)", v_optional_slug, default="")
    else:
        slug = ""
    slug = slug.lower()
    if v_optional_slug(slug):
        p.error(f"slug: {v_optional_slug(slug)}")
    folder = f"{pid}-{slug}" if slug and slug != pid else pid

    target = platform_dir / folder
    title = a.title or ask("문제 제목")
    url = a.url or ask("문제 URL", v_url)
    level = a.level or ask("플랫폼 표기 레벨 (예: Lv.2 / D3 / Silver 2 / 중급)")
    print("  공통 난이도: " + ", ".join(f"{k}={v}" for k, v in DIFFICULTY_LABELS.items()))
    difficulty = a.difficulty or ask("공통 난이도 (1~5)", v_difficulty)
    if v_difficulty(difficulty):
        p.error(f"difficulty: {v_difficulty(difficulty)}")
    tags = a.tags or ask("태그 (쉼표로 구분, 예: BFS,그래프)")
    proposer = a.proposer or ask("내 GitHub ID")

    tag_list = ", ".join(t.strip() for t in tags.split(",") if t.strip())
    content = render_template(TEMPLATES_DIR / "problem.md", {
        "title": title,
        "platform": platform,
        "id": pid,
        "url": url,
        "level": level,
        "difficulty": difficulty,
        "tags": tag_list,
        "proposer": proposer,
        "added": date.today().isoformat(),
    })

    (target / "solutions").mkdir(parents=True)
    (target / "README.md").write_text(content, encoding="utf-8", newline="\n")
    (target / "solutions" / ".gitkeep").touch()

    rel = target.relative_to(ROOT).as_posix()
    print(f"\n생성 완료: {rel}/")
    print(f"  1) {rel}/README.md 의 '문제 요약'과 '핵심 포인트'를 직접 작성하세요 (원문 복사 금지)")
    print(f"  2) 풀이도 함께 올리려면: python scripts/new_solution.py {rel} --author {proposer} --lang py")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print("\n취소했습니다.")
        sys.exit(130)
