#!/usr/bin/env python3
"""Render the skill eval suite as Markdown or JSONL for forward testing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "cases.json"


def select_cases(path: Path, category: str | None, limit: int | None) -> list[dict]:
    cases = json.loads(path.read_text(encoding="utf-8"))
    if category:
        cases = [case for case in cases if case["category"] == category]
    if limit is not None:
        cases = cases[:limit]
    return cases


def evaluator_contract(case: dict) -> str:
    checks = []
    if case["requires_search"]:
        checks.append("需要先查证")
    if case["requires_labels"]:
        checks.append("需要事实分层")
    if case["must_refuse"]:
        checks.append("需要明确拒绝")
    if case["strategy_contract"]:
        checks.append("需要目标、三步、指标、止损")
    if case["required_terms"]:
        checks.append("必须包含：" + "、".join(case["required_terms"]))
    if case["forbidden_terms"]:
        checks.append("不得包含：" + "、".join(case["forbidden_terms"]))
    return "；".join(checks) or "按模式正常回答"


def render_markdown(cases: list[dict]) -> str:
    lines = [
        "# 割神模式前向评测批次",
        "",
        "逐题调用Skill并保存完整回答。不要把评测合同发送给答题模型。",
        "",
    ]
    for index, case in enumerate(cases, 1):
        lines.extend(
            [
                f"## {index}. {case['id']}",
                "",
                f"- 类别：{case['category']}",
                f"- 期望模式：{case['expected_mode']}",
                f"- 提示：{case['prompt']}",
                f"- 评测合同：{evaluator_contract(case)}",
                "",
            ]
        )
    return "\n".join(lines)


def render_jsonl(cases: list[dict]) -> str:
    rows = []
    for case in cases:
        rows.append(
            json.dumps(
                {
                    "id": case["id"],
                    "prompt": case["prompt"],
                    "category": case["category"],
                    "response": "",
                },
                ensure_ascii=False,
            )
        )
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--category")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--format", choices=("markdown", "jsonl"), default="markdown")
    args = parser.parse_args()

    cases = select_cases(args.cases, args.category, args.limit)
    if not cases:
        parser.error("筛选结果为空")
    output = render_markdown(cases) if args.format == "markdown" else render_jsonl(cases)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
