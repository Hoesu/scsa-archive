"""저장소에 표준 라벨 세트를 만든다. (관리자가 최초 1회 실행)

준비: GitHub CLI 설치 후 로그인 -> https://cli.github.com
    gh auth login

사용법:
    python scripts/setup_labels.py                       # 현재 폴더의 origin 저장소
    python scripts/setup_labels.py --repo owner/name     # 저장소 직접 지정

이미 있는 라벨은 색/설명만 갱신한다. (--force)
"""

from __future__ import annotations

import argparse
import subprocess
import sys

from common import setup_console

# (이름, 색상, 설명)  -- .github/labeler.yml, ISSUE_TEMPLATE 과 이름을 맞춰야 한다
LABELS = [
    # 유형
    ("문제-제안", "1d76db", "새로운 문제를 은행에 추가하자는 제안"),
    ("문제-등록", "0e8a16", "문제 폴더(README)를 추가하는 PR"),
    ("풀이", "5319e7", "풀이 코드를 추가/수정하는 PR"),
    ("질문", "d876e3", "풀이나 문제에 대한 질문"),
    ("문서", "0075ca", "README, 가이드 문서 수정"),
    ("개선", "a2eeef", "스크립트, 템플릿, 자동화 개선"),
    # 상태
    ("채택", "2ea44f", "제안이 채택됨 - 등록 PR을 올려주세요"),
    ("보류", "fbca04", "논의가 더 필요함"),
    ("중복", "cfd3d7", "이미 등록되었거나 중복된 제안"),
    ("리뷰-환영", "fef2c0", "누구든 리뷰해주면 좋은 PR"),
    ("good first issue", "7057ff", "처음 기여하기 좋은 이슈"),
    # 플랫폼
    ("platform:codetree", "f9d0c4", "Codetree"),
    ("platform:swea", "f9d0c4", "SW Expert Academy"),
    ("platform:programmers", "f9d0c4", "Programmers"),
    ("platform:boj", "f9d0c4", "Baekjoon"),
    ("platform:leetcode", "f9d0c4", "LeetCode"),
    ("platform:etc", "f9d0c4", "기타 플랫폼"),
    # 난이도 (공통 척도)
    ("난이도:1", "c2e0c6", "입문"),
    ("난이도:2", "9fdfa9", "기초"),
    ("난이도:3", "fbe38e", "중급"),
    ("난이도:4", "f4a261", "상급"),
    ("난이도:5", "e63946", "최상급"),
]


def main() -> int:
    setup_console()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--repo", help="owner/name (생략 시 현재 저장소)")
    a = p.parse_args()

    repo_args = ["--repo", a.repo] if a.repo else []
    failed = 0
    for name, color, desc in LABELS:
        cmd = ["gh", "label", "create", name, "--color", color, "--description", desc, "--force", *repo_args]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"  ok  {name}")
        except FileNotFoundError:
            print("GitHub CLI(gh)가 없습니다. https://cli.github.com 에서 설치 후 'gh auth login' 하세요.")
            return 1
        except subprocess.CalledProcessError as e:
            failed += 1
            print(f"  실패 {name}: {e.stderr.strip()}")
    print(f"\n라벨 {len(LABELS) - failed}/{len(LABELS)}개 적용 완료")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
