"""문제를 검색해서 내 풀이 파일을 템플릿으로 만든다.

사용법:
    python scripts/new_solution.py 아기         # 제목/id/폴더명 일부로 검색 (띄어쓰기·대소문자 무시)
    python scripts/new_solution.py 12906        # id 를 정확히 치면 바로 선택
    python scripts/new_solution.py              # 목록에서 번호로 고르기 (풀이 없는 문제가 먼저)
    python scripts/new_solution.py 12906 --variant dp      # 같은 문제의 두 번째 풀이 (hoesu_dp.py)

- 내 GitHub ID 는 처음 한 번만 묻고 이 저장소의 git 설정(scsa.author)에 저장한다.
  바꾸려면: git config scsa.author <새 ID>
- main 브랜치에서 실행하면 main 을 최신으로 받고 solve/<ID>/<플랫폼>-<id> 브랜치를 자동으로 만든다.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from common import (
    PLATFORMS,
    ROOT,
    SOLUTION_EXT,
    SOLUTION_FILE_RE,
    TEMPLATES_DIR,
    current_branch,
    git,
    iter_problem_dirs,
    iter_solution_files,
    nfc,
    parse_front_matter,
    render_template,
    setup_console,
    switch_branch,
    update_main,
)

AUTHOR_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$")
VARIANT_RE = re.compile(r"^[a-z0-9-]+$")


class Cancelled(Exception):
    pass


def norm(s: str) -> str:
    return re.sub(r"[\s-]+", "", nfc(s)).lower()


# ---------------------------------------------------------------- 내 GitHub ID

def resolve_author(given: str | None) -> str:
    if given:
        if not AUTHOR_RE.match(given):
            sys.exit(f"GitHub ID 형식이 아닙니다: {given}")
        return given
    saved = git("config", "--get", "scsa.author").stdout.strip()
    if saved:
        return saved
    print("처음 한 번만 내 GitHub ID 를 입력해 주세요. (풀이 파일 이름이 됩니다)")
    while True:
        author = input("내 GitHub ID: ").strip()
        if AUTHOR_RE.match(author):
            break
        print("  -> 영문/숫자/하이픈만 사용합니다")
    git("config", "scsa.author", author)
    print(f"  저장했습니다. 다음부터는 묻지 않아요. (바꾸려면: git config scsa.author <새 ID>)\n")
    return author


# ---------------------------------------------------------------- 문제 검색

def load_problems(author: str) -> list[dict]:
    problems = []
    for d in iter_problem_dirs():
        try:
            meta = parse_front_matter((d / "README.md").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        authors = []
        for f in iter_solution_files(d):
            m = SOLUTION_FILE_RE.match(f.name)
            if m:
                authors.append(m["author"].lower())
        platform = d.parent.name
        problems.append({
            "dir": d,
            "rel": d.relative_to(ROOT).as_posix(),
            "platform": platform,
            "id": str(meta.get("id", d.name)),
            "title": meta.get("title", d.name),
            "url": meta.get("url", ""),
            "count": len(authors),
            "mine": author.lower() in authors,
        })
    # 풀이 없는 문제 먼저, 그다음 플랫폼/제목 순
    problems.sort(key=lambda p: (p["count"] > 0, p["platform"], p["title"]))
    return problems


def search(problems: list[dict], query: str) -> list[dict]:
    q = norm(query)
    exact = [p for p in problems if q in (norm(p["id"]), norm(p["dir"].name), norm(p["title"]))]
    if len(exact) == 1:
        return exact
    return [
        p for p in problems
        if any(q in norm(s) for s in (p["title"], p["id"], p["dir"].name, p["platform"], PLATFORMS.get(p["platform"], "")))
    ]


def describe(p: dict) -> str:
    mine = " (내 풀이 있음)" if p["mine"] else ""
    return f"[{PLATFORMS.get(p['platform'], p['platform'])}] {p['title']}  - 풀이 {p['count']}개{mine}"


def choose(cands: list[dict], header: str) -> dict:
    print(header)
    for i, p in enumerate(cands, 1):
        print(f"  {i:>2}) {describe(p)}")
    while True:
        s = input("번호를 고르세요 (취소: Enter): ").strip()
        if not s:
            raise Cancelled
        if s.isdigit() and 1 <= int(s) <= len(cands):
            return cands[int(s) - 1]
        print(f"  -> 1~{len(cands)} 사이 번호를 입력하세요")


def confirm(question: str) -> bool:
    return input(f"{question} [Y/n]: ").strip().lower() in ("", "y", "yes", "ㅛ")


def pick_problem(problems: list[dict], query: str | None) -> dict:
    if not problems:
        sys.exit("등록된 문제가 없습니다. 먼저 문제를 등록하세요: python scripts/new_problem.py --issue <번호>")
    while True:
        if not query:
            return choose(problems, "전체 문제 (풀이가 없는 문제가 먼저 나옵니다):")
        found = search(problems, query)
        if len(found) == 1:
            p = found[0]
            print(f"-> {describe(p)}\n   {p['rel']}")
            if confirm("이 문제가 맞나요?"):
                return p
            query = input("다시 검색 (Enter: 전체 목록): ").strip()
        elif found:
            return choose(found, f'"{query}" 에 해당하는 문제가 {len(found)}개 있습니다:')
        else:
            print(f'"{query}" 에 해당하는 문제가 없습니다.')
            print("  - 다른 단어로 다시 검색하거나 Enter 로 전체 목록을 보세요")
            print("  - 최근에 등록된 문제라면 git pull 로 최신 내용을 받아보세요")
            print("  - 아직 등록되지 않은 문제라면 먼저 등록하세요: python scripts/new_problem.py --issue <번호>")
            query = input("다시 검색: ").strip()
        print()


# ---------------------------------------------------------------- 풀이 파일

def pick_variant(problem: dict, author: str, variant: str | None) -> str | None:
    solutions = problem["dir"] / "solutions"
    if variant is None and not problem["mine"]:
        return None
    if variant is None:
        mine = [f.name for f in iter_solution_files(problem["dir"])
                if (m := SOLUTION_FILE_RE.match(f.name)) and m["author"].lower() == author.lower()]
        print(f"이미 내 풀이가 있습니다: {', '.join(mine)}")
        print("두 번째 풀이로 만들려면 구분 이름을 입력하세요. (예: dp, bfs → " + f"{author}_dp.py)")
    while True:
        if variant is None:
            variant = input("구분 이름 (취소: Enter): ").strip().lower()
            if not variant:
                raise Cancelled
        if not VARIANT_RE.match(variant):
            print("  -> 소문자/숫자/하이픈만 사용합니다")
        elif (solutions / f"{author}_{variant}{SOLUTION_EXT}").exists():
            print(f"  -> {author}_{variant}{SOLUTION_EXT} 도 이미 있습니다. 다른 이름을 입력하세요")
        else:
            return variant
        variant = None


def ensure_branch(problem: dict, author: str) -> str:
    current = current_branch()
    if current != "main":
        return current
    branch = f"solve/{author}/{problem['platform']}-{problem['id'].lower()}"
    switch_branch(branch)
    return branch


def main() -> int:
    setup_console()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query", nargs="?", help="문제 제목/id/폴더명 일부, 또는 문제 폴더 경로 (생략하면 목록에서 선택)")
    p.add_argument("--author", help="내 GitHub ID (생략하면 저장된 값 사용)")
    p.add_argument("--variant", help="같은 문제에 두 번째 풀이를 올릴 때 구분 이름 (예: dp, bfs)")
    a = p.parse_args()

    author = resolve_author(a.author)
    update_main()
    problems = load_problems(author)

    # 예전 방식처럼 폴더 경로를 그대로 준 경우
    as_path = Path(a.query).resolve() if a.query else None
    by_path = [x for x in problems if as_path and x["dir"] == as_path]
    problem = by_path[0] if by_path else pick_problem(problems, a.query)
    print()

    variant = pick_variant(problem, author, a.variant.lower() if a.variant else None)
    branch = ensure_branch(problem, author)

    target = problem["dir"] / "solutions" / f"{author}{f'_{variant}' if variant else ''}{SOLUTION_EXT}"
    content = render_template(TEMPLATES_DIR / f"solution{SOLUTION_EXT}", {
        "title": problem["title"],
        "platform": PLATFORMS.get(problem["platform"], problem["platform"]),
        "id": problem["id"],
        "url": problem["url"],
        "author": author,
    })
    target.parent.mkdir(exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    gitkeep = target.parent / ".gitkeep"
    if gitkeep.exists():
        gitkeep.unlink()

    rel = target.relative_to(ROOT).as_posix()
    print(f"\n생성 완료: {rel}\n")
    print("다음 단계:")
    print(f"  1) {rel} 를 열어 헤더(결과, 접근)와 코드를 작성 (복잡도는 선택)")
    print("  2) python scripts/validate.py")
    print("  3) 아래 세 줄을 그대로 실행")
    print("     git add problems/")
    print(f"     git commit -m \"[풀이] {problem['title']}\"")
    print(f"     git push -u origin {branch}")
    print("  4) GitHub 저장소 페이지의 Compare & pull request 버튼으로 PR 만들기")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError, Cancelled):
        print("\n취소했습니다.")
        sys.exit(130)
