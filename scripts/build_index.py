"""problems/ 를 훑어서 PROBLEMS.md (전체 문제 목록)를 생성한다.

사용법:
    python scripts/build_index.py

main 브랜치에 머지되면 GitHub Actions가 자동으로 실행하므로,
PR에서 PROBLEMS.md 를 직접 수정할 필요는 없다. (충돌의 원인이 됨)
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict

from common import (
    DIFFICULTY_LABELS,
    PLATFORMS,
    ROOT,
    SOLUTION_FILE_RE,
    iter_problem_dirs,
    iter_solution_files,
    parse_front_matter,
    setup_console,
)

OUTPUT = ROOT / "PROBLEMS.md"


def collect():
    problems = []
    for problem_dir in iter_problem_dirs():
        readme = problem_dir / "README.md"
        try:
            meta = parse_front_matter(readme.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue  # 형식 오류는 validate.py 가 잡는다
        authors = set()
        solution_count = 0
        for f in iter_solution_files(problem_dir):
            m = SOLUTION_FILE_RE.match(f.name)
            if not m:
                continue
            solution_count += 1
            authors.add(m["author"].lower())
        tags = meta.get("tags") if isinstance(meta.get("tags"), list) else []
        problems.append({
            "path": problem_dir.relative_to(ROOT).as_posix(),
            "platform": problem_dir.parent.name,
            "title": meta.get("title", problem_dir.name),
            "id": meta.get("id", ""),
            "url": meta.get("url", ""),
            "level": meta.get("level", "-"),
            "difficulty": int(meta["difficulty"]) if str(meta.get("difficulty", "")).isdigit() else 0,
            "tags": tags,
            "authors": authors,
            "solution_count": solution_count,
        })
    return problems


def render(problems) -> str:
    out = [
        "# 전체 문제 목록",
        "",
        "> 이 파일은 `scripts/build_index.py` 가 자동으로 생성합니다. **직접 수정하지 마세요.**",
        "",
    ]

    total_solutions = sum(p["solution_count"] for p in problems)
    by_platform = defaultdict(list)
    for p in problems:
        by_platform[p["platform"]].append(p)

    out += [
        "## 요약",
        "",
        f"- 문제 **{len(problems)}**개 · 풀이 **{total_solutions}**개",
        "- 플랫폼별: " + (" · ".join(
            f"{PLATFORMS.get(k, k)} {len(v)}" for k, v in sorted(by_platform.items())
        ) or "없음"),
        "",
        "난이도는 플랫폼 간 비교를 위한 공통 척도입니다: "
        + ", ".join(f"`{k}` {v}" for k, v in DIFFICULTY_LABELS.items()),
        "",
    ]

    for platform in PLATFORMS:
        items = by_platform.get(platform)
        if not items:
            continue
        items.sort(key=lambda p: (p["difficulty"], int(p["id"]) if p["id"].isdigit() else 0, p["id"]))
        out += [
            f"## {PLATFORMS[platform]}",
            "",
            "| 문제 | 레벨 | 난이도 | 태그 | 풀이 | 원문 |",
            "|---|---|:---:|---|:---:|:---:|",
        ]
        for p in items:
            stars = "★" * p["difficulty"] if p["difficulty"] else "-"
            tags = " ".join(f"`{t}`" for t in p["tags"]) or "-"
            link = f"[링크]({p['url']})" if p["url"] else "-"
            out.append(
                f"| [{p['id']}. {p['title']}]({p['path']}) | {p['level']} | {stars} "
                f"| {tags} | {p['solution_count']} | {link} |"
            )
        out.append("")

    tag_map = defaultdict(list)
    for p in problems:
        for t in p["tags"]:
            tag_map[t].append(p)
    if tag_map:
        out += ["## 태그별 보기", ""]
        for tag in sorted(tag_map, key=lambda t: (-len(tag_map[t]), t)):
            links = ", ".join(f"[{p['title']}]({p['path']})" for p in tag_map[tag])
            out.append(f"- **{tag}** ({len(tag_map[tag])}): {links}")
        out.append("")

    solved = Counter()
    for p in problems:
        for a in p["authors"]:
            solved[a] += 1
    if solved:
        out += [
            "## 풀이 기여 현황",
            "",
            "| 순위 | GitHub ID | 푼 문제 수 |",
            "|:---:|---|:---:|",
        ]
        for rank, (author, n) in enumerate(sorted(solved.items(), key=lambda x: (-x[1], x[0])), 1):
            out.append(f"| {rank} | [@{author}](https://github.com/{author}) | {n} |")
        out.append("")

    return "\n".join(out)


def main() -> int:
    setup_console()
    problems = collect()
    OUTPUT.write_text(render(problems), encoding="utf-8", newline="\n")
    print(f"PROBLEMS.md 생성 완료: 문제 {len(problems)}개")
    return 0


if __name__ == "__main__":
    sys.exit(main())
