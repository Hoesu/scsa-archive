"""새 문제 폴더를 템플릿으로 만든다.

사용법:
    python scripts/new_problem.py --issue 4     # 문제 제안 이슈 내용을 그대로 가져온다 (권장)
    python scripts/new_problem.py               # 인자를 생략하면 하나씩 물어본다
    python scripts/new_problem.py --platform programmers --id 12906 --slug same-numbers \\
        --title "같은 숫자는 싫어" --url https://school.programmers.co.kr/learn/courses/30/lessons/12906 \\
        --level Lv.1 --difficulty 1 --tags "스택/큐,구현" --proposer hoesu

--issue 와 다른 인자를 함께 주면 직접 준 인자가 우선한다.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date

from common import (
    DIFFICULTY_LABELS,
    PLATFORMS,
    PROBLEM_DIR_RE,
    PROBLEMS_DIR,
    REPO,
    ROOT,
    TEMPLATES_DIR,
    render_template,
    setup_console,
)

# 문제 제안 이슈 폼(.github/ISSUE_TEMPLATE/01-problem-proposal.yml)의 label -> 인자 이름
ISSUE_FIELDS = {
    "플랫폼": "platform",
    "문제 번호 / id": "id",
    "문제 제목": "title",
    "문제 링크": "url",
    "플랫폼 표기 레벨": "level",
    "체감 난이도 (공통 척도)": "difficulty",
    "알고리즘 분류 (태그)": "tags",
    "추천 이유": "reason",
}

REASON_PLACEHOLDER = "<!-- 어떤 유형을 연습하기 좋은지, 시험에 자주 나오는 패턴인지 등 -->"


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


def fetch_issue(number: int) -> dict:
    """GitHub API 로 이슈를 읽는다. 공개 저장소라 로그인 없이 동작한다."""
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/issues/{number}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "scsa-archive"},
    )
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit(f"이슈 #{number} 를 찾을 수 없습니다. 번호를 확인하세요.")
        if e.code == 403:
            sys.exit("GitHub API 호출 한도를 넘었습니다. 잠시 후 다시 하거나, 인자로 직접 입력하세요.")
        sys.exit(f"이슈를 가져오지 못했습니다 (HTTP {e.code})")
    except urllib.error.URLError as e:
        sys.exit(f"GitHub 에 연결할 수 없습니다: {e.reason}")


def parse_issue_form(body: str) -> dict:
    """이슈 폼 본문(### 라벨 / 값 반복)을 {인자 이름: 값} 으로 바꾼다."""
    body = body.replace("\r\n", "\n")
    values = {}
    for m in re.finditer(r"^### (.+?)[ \t]*\n(.*?)(?=^### |\Z)", body, re.S | re.M):
        key = ISSUE_FIELDS.get(m[1].strip())
        value = m[2].strip()
        if key and value and value != "_No response_":
            values[key] = value
    if "difficulty" in values:
        values["difficulty"] = values["difficulty"][:1]  # "4 - 상급" -> "4"
    return values


def current_branch() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def main() -> int:
    setup_console()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--issue", type=int, help="문제 제안 이슈 번호 (이슈에 적힌 정보를 자동으로 채움)")
    for name in ("platform", "id", "slug", "title", "url", "level", "difficulty", "tags", "proposer"):
        p.add_argument(f"--{name}")
    a = p.parse_args()

    print("새 문제 등록 (Ctrl+C 로 취소)\n")

    found: dict = {}
    title_default = None
    if a.issue:
        issue = fetch_issue(a.issue)
        if "pull_request" in issue:
            p.error(f"#{a.issue} 는 이슈가 아니라 PR 입니다")
        found = parse_issue_form(issue.get("body") or "")
        found["proposer"] = issue["user"]["login"]
        labels = {label["name"] for label in issue.get("labels", [])}
        print(f"이슈 #{a.issue} 「{issue['title']}」 에서 정보를 가져왔습니다.")
        if "채택" not in labels:
            print("  * 아직 '채택' 라벨이 없는 이슈입니다. 등록 전에 채택 여부를 확인하세요.")
        if "title" not in found:
            # 문제 제목 칸이 생기기 전에 작성된 이슈: 이슈 제목을 기본값으로 제안
            title_default = re.sub(r"^\[제안\]\s*", "", issue["title"]).strip() or None
        for key in ("platform", "id", "title", "url", "level", "difficulty", "tags", "proposer"):
            if key in found:
                print(f"  {key:<10} {found[key]}")
        print()

    def get(name: str):
        return getattr(a, name) or found.get(name)

    platform = get("platform") or ask(f"플랫폼 ({'/'.join(PLATFORMS)})", v_platform)
    if v_platform(platform):
        p.error(v_platform(platform))

    if not get("id") and platform == "codetree":
        print("  * Codetree 는 문제 번호가 없으므로 URL 마지막의 영문 이름을 id 로 씁니다 (예: maze-escape)")
    pid = (get("id") or ask("문제 id (번호 또는 영문 slug)", v_slug)).lower()
    if v_slug(pid):
        p.error(f"id: {v_slug(pid)}")

    platform_dir = PROBLEMS_DIR / platform
    existing = [d for d in platform_dir.glob(f"{pid}*") if d.is_dir() and re.match(rf"^{re.escape(pid)}(-|$)", d.name)]
    if existing:
        rel = existing[0].relative_to(ROOT).as_posix()
        print(f"\n이미 등록된 문제입니다: {rel}")
        print(f"풀이만 추가하려면: python scripts/new_solution.py {rel} --author <github-id>")
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
    title = get("title") or ask("문제 제목 (플랫폼 표기 그대로)", default=title_default)
    url = get("url") or ask("문제 URL", v_url)
    if v_url(url):
        p.error(f"url: {v_url(url)}")
    level = get("level") or ask("플랫폼 표기 레벨 (예: Lv.2 / D3 / Silver 2 / 중급)")
    if not get("difficulty"):
        print("  공통 난이도: " + ", ".join(f"{k}={v}" for k, v in DIFFICULTY_LABELS.items()))
    difficulty = get("difficulty") or ask("공통 난이도 (1~5)", v_difficulty)
    if v_difficulty(difficulty):
        p.error(f"difficulty: {v_difficulty(difficulty)}")
    tags = get("tags") or ask("태그 (쉼표로 구분, 예: BFS,그래프)")
    proposer = get("proposer") or ask("제안자 GitHub ID")

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
        "reason": found.get("reason", REASON_PLACEHOLDER),
    })

    (target / "solutions").mkdir(parents=True)
    (target / "README.md").write_text(content, encoding="utf-8", newline="\n")
    (target / "solutions" / ".gitkeep").touch()

    rel = target.relative_to(ROOT).as_posix()
    branch = f"problem/{platform}-{pid}"
    print(f"\n생성 완료: {rel}/\n")
    print("다음 단계:")
    if current_branch() in ("main", ""):
        print(f"  0) 지금 main 브랜치입니다. 먼저 브랜치를 만드세요 (만든 파일은 그대로 따라옵니다)")
        print(f"     git switch -c {branch}")
    print(f"  1) {rel}/README.md 의 '문제 요약', '핵심 포인트', '힌트'를 직접 작성 (원문 복사 금지)")
    print("  2) python scripts/validate.py")
    print(f"  3) git add problems/ && git commit -m \"[문제] {title}\"")
    print(f"  4) git push -u origin {current_branch() if current_branch() not in ('main', '') else branch}")
    if a.issue:
        print(f"  5) PR 본문에 'Closes #{a.issue}' 한 줄을 적으면 머지 때 이슈가 자동으로 닫힙니다")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print("\n취소했습니다.")
        sys.exit(130)
