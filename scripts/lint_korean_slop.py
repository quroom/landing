#!/usr/bin/env python3
"""Korean AI Slop & Copywriting Tone Linter for QUROOM.

Scans project files for:
  1. Robotic AI section headers & repetitive lazy predicates (e.g. '이런 경우에 적합합니다', '무엇을 먼저 할지 정리합니다')
  2. Banned AI marketing buzzwords & slop tropes (e.g. '혁신적인', '압도적인', '대참사', '완벽한')
  3. Immutable fact constraints (e.g. founder experience must be '8년 차', not '10년 차')
"""

from __future__ import annotations

import glob
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SlopRule:
    rule_id: str
    pattern: re.Pattern[str]
    message: str
    suggestion: str


RULES: list[SlopRule] = [
    # 1. Robotic AI structural clichés
    SlopRule(
        rule_id="ai-cliche-fit-header",
        pattern=re.compile(r"이런\s*경우에\s*적합합니다"),
        message="AI-slop header: Typical machine-generated recommendation title.",
        suggestion="대체: '이런 프로젝트에 알맞습니다' / '주요 제작 의뢰 목적' / '이런 상황에 권장합니다'",
    ),
    SlopRule(
        rule_id="ai-cliche-lazy-organize-header",
        pattern=re.compile(r"무엇을\s*먼저\s*할지\s*정리합니다"),
        message="AI-slop header: Vague machine-generated outcome predicate.",
        suggestion="대체: '착수 전 개발 우선순위 기준' / '개발 범위와 우선순위부터 나눕니다'",
    ),
    # 2. Banned hyperbole & emotional drama (AGENTS.md)
    SlopRule(
        rule_id="banned-buzzword-extreme",
        pattern=re.compile(
            r"\b(대참사|기적\s*같은|압도적인|게임체인저|폭발적인|소명\s*지옥|피눈물)\b"
        ),
        message="Banned marketing trope: Hyperbolic or overly dramatic expression.",
        suggestion="자극적 과장 표현을 삭제하고 사실 위주의 엔지니어 문장으로 변경하십시오.",
    ),
    SlopRule(
        rule_id="banned-buzzword-slop",
        pattern=re.compile(r"\b(혁신적인|완벽한|기적의|단숨에)\b"),
        message="Banned AI slop: Low-information promotional modifier.",
        suggestion="구체적인 기술 스택이나 작동 방식으로 서술하십시오.",
    ),
    SlopRule(
        rule_id="banned-unrealistic-metric",
        pattern=re.compile(
            r"(0\.1초\s*만에|30분\s*만에\s*앱\s*완성|매출\s*300%|10분\s*만에\s*끝내는)"
        ),
        message="Banned AI trope: Unrealistic promotional metrics.",
        suggestion="실제 검증 가능한 일정과 공수를 명시하십시오.",
    ),
    SlopRule(
        rule_id="banned-guarantee",
        pattern=re.compile(
            r"(100%\s*분쟁\s*방지|회계감사\s*프리패스|합격\s*보장|보완이나\s*반려\s*없이)"
        ),
        message="Banned guarantee: Misleading contractual guarantee.",
        suggestion="객관적인 절차 및 보완 프로세스를 명시하십시오.",
    ),
    # 3. Patronizing AI expressions & lazy predicates
    SlopRule(
        rule_id="ai-condescending-permission",
        pattern=re.compile(r"(?:않아도|않았어도|안\s*돼도)\s*괜찮습니다"),
        message="Patronizing AI phrasing: Overly comforting 'It is okay even if unorganized/unprepared'.",
        suggestion="구체적이고 정중한 협업 제안 문구로 수정하십시오 (예: '완성된 기획서가 없어도 좋습니다', '프로젝트 구상 단계에서도 편하게 남겨주세요').",
    ),
    SlopRule(
        rule_id="ai-lazy-split-predicate",
        pattern=re.compile(r"기능부터\s*나눕니다|확정합니다"),
        message="Lazy AI predicate: Defensively splitting/chopping features.",
        suggestion="출시 범위와 우선순위를 함께 설계하는 문장으로 변경하십시오.",
    ),
    SlopRule(
        rule_id="ai-unverified-percentage",
        pattern=re.compile(r"분쟁의\s*(?:\d+(?:\.\d+)?\s*%|상당수|대부분)"),
        message="Unverified statistical hyperbole: '90%' dispute figure.",
        suggestion="빈도나 비율 대신 분쟁이 생길 수 있는 조건과 원인을 설명하십시오.",
    ),
    # 4. Founder experience integrity constraint
    SlopRule(
        rule_id="founder-career-mismatch",
        pattern=re.compile(r"10년\s*(?:차|이상)"),
        message="Company fact violation: Founder experience must strictly be '8년 차'.",
        suggestion="'8년 차'로 수정하십시오.",
    ),
]

SCAN_TARGETS = [
    "landing/content.py",
    "landing/ad_landing.py",
    "landing/forms.py",
    "landing/templates/landing/**/*.html",
]

EXCLUDE_PATTERNS = [
    "landing/templates/landing/admin_*.html",
    "landing/templates/landing/privacy.html",
    "landing/templates/landing/terms.html",
    "**/node_modules/**",
]


def is_excluded(path_str: str) -> bool:
    path_obj = Path(path_str)
    for exc in EXCLUDE_PATTERNS:
        if path_obj.match(exc):
            return True
    return False


def collect_files(root_dir: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in SCAN_TARGETS:
        full_pattern = str(root_dir / pattern)
        for match in glob.glob(full_pattern, recursive=True):
            p = Path(match)
            rel_str = str(p.relative_to(root_dir))
            if not is_excluded(rel_str) and p.is_file():
                files.append(p)
    return sorted(set(files))


def scan_file(file_path: Path, root_dir: Path) -> list[str]:
    findings: list[str] = []
    rel_path = file_path.relative_to(root_dir)
    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()
    except Exception as err:
        findings.append(f"{rel_path}:0:0 [read-error] {err}")
        return findings

    for line_idx, line in enumerate(lines, start=1):
        if "slop-gate-ignore" in line or "slop-lint-ignore" in line:
            continue
        for rule in RULES:
            for m in rule.pattern.finditer(line):
                col = m.start() + 1
                matched_text = m.group(0)
                findings.append(
                    f"{rel_path}:{line_idx}:{col}  {matched_text}\n"
                    f"  [{rule.rule_id}] {rule.message}\n"
                    f"  💡 {rule.suggestion}"
                )
    return findings


def main() -> int:
    root_dir = Path(__file__).resolve().parent.parent
    files = collect_files(root_dir)
    all_findings: list[str] = []

    for f in files:
        all_findings.extend(scan_file(f, root_dir))

    print(f"[korean-slop-lint] Scanned {len(files)} files.")
    if all_findings:
        print(f"\n❌ Found {len(all_findings)} AI slop / copy issue(s):\n")
        for finding in all_findings:
            print(finding)
        print("\nPlease fix these copy issues before deploying.\n")
        return 1

    print("✅ All files clean from Korean AI slop & forbidden tropes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
