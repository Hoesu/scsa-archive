"""problems/ 를 훑어서 PROBLEMS.md (전체 문제 목록)를 생성한다.

사용법:
    python scripts/build_index.py                     # 미리 보기 (저장소 루트에 생성, .gitignore 대상)
    python scripts/build_index.py --output <경로>

main 에 머지되면 GitHub Actions 가 실행해서 결과를 index 브랜치에 올린다.
main 은 보호 규칙 때문에 봇이 직접 커밋할 수 없으므로 목록은 별도 브랜치에 둔다.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

from common import (
    DIFFICULTY_LABELS,
    PLATFORMS,
    REPO_URL,
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
            "rel": problem_dir.relative_to(ROOT).as_posix(),
            "path": f"{REPO_URL}/tree/main/{quote(problem_dir.relative_to(ROOT).as_posix())}",
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
        "> 이 파일은 main 에 머지될 때마다 `scripts/build_index.py` 가 자동으로 생성해 `index` 브랜치에 올립니다. **직접 수정하지 마세요.**",
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

    waiting = sorted((p for p in problems if p["solution_count"] == 0), key=lambda p: (p["difficulty"], p["rel"]))
    if waiting:
        out += [
            f"## 풀이를 기다리는 문제 ({len(waiting)})",
            "",
            "아직 아무도 풀이를 올리지 않은 문제입니다. 첫 풀이의 주인공이 되어 주세요!",
            "풀이 파일 만들기: `python scripts/new_solution.py <문제 이름 일부>`",
            "",
            "| 문제 | 플랫폼 | 난이도 | 경로 |",
            "|---|---|:---:|---|",
        ]
        for p in waiting:
            stars = "★" * p["difficulty"] if p["difficulty"] else "-"
            out.append(f"| [{p['title']}]({p['path']}) | {PLATFORMS.get(p['platform'], p['platform'])} | {stars} | `{p['rel']}` |")
        out.append("")

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
            name = f"{p['id']}. {p['title']}" if p["id"].isdigit() else p["title"]
            out.append(
                f"| [{name}]({p['path']}) | {p['level']} | {stars} "
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
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--output", type=Path, default=OUTPUT, help="결과 파일 경로 (기본: 저장소 루트의 PROBLEMS.md)")
    a = p.parse_args()

    problems = collect()
    a.output.write_text(render(problems), encoding="utf-8", newline="\n")
    print(f"{a.output} 생성 완료: 문제 {len(problems)}개")
    return 0


if __name__ == "__main__":
    sys.exit(main())
