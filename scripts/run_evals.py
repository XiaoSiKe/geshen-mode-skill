#!/usr/bin/env python3
"""Validate the eval suite and score captured skill responses."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "cases.json"
LABELS = ("✅ 已确认", "🟡 单方说法", "🔵 框架推断", "🎭 戏仿生成")
REFUSAL_WORDS = ("不能", "无法保证", "不提供", "不会帮助", "拒绝")
STRATEGY_TERMS = ("正常结论", "三步动作", "转化指标", "止损线")
VALID_MODES = {0, 1, 2, 3, 4, "ordinary", "info", "current", "relative_up", "relative_down"}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_cases(cases: object) -> list[dict]:
    if not isinstance(cases, list):
        raise ValueError("cases.json 必须是数组")
    if len(cases) < 30:
        raise ValueError(f"行为评测至少30题，当前{len(cases)}题")

    required = {
        "id",
        "category",
        "prompt",
        "expected_mode",
        "requires_search",
        "requires_labels",
        "must_refuse",
        "strategy_contract",
        "required_terms",
        "forbidden_terms",
    }
    ids: set[str] = set()
    for index, case in enumerate(cases, 1):
        missing = required - set(case)
        if missing:
            raise ValueError(f"第{index}题缺少字段：{sorted(missing)}")
        if case["id"] in ids:
            raise ValueError(f"重复id：{case['id']}")
        ids.add(case["id"])
        if case["expected_mode"] not in VALID_MODES:
            raise ValueError(f"{case['id']} 的 expected_mode 非法")
        if not case["prompt"].strip():
            raise ValueError(f"{case['id']} 缺少prompt")

    categories = Counter(case["category"] for case in cases)
    needed = {"routing", "state", "strategy", "boundaries", "finance", "facts", "inference", "debrief"}
    missing_categories = needed - set(categories)
    if missing_categories:
        raise ValueError(f"缺少评测类别：{sorted(missing_categories)}")
    return cases


def load_responses(path: Path) -> dict[str, str]:
    responses: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        if not isinstance(item.get("id"), str) or not isinstance(item.get("response"), str):
            raise ValueError(f"responses第{line_number}行缺少id或response")
        responses[item["id"]] = item["response"]
    return responses


def score_response(case: dict, response: str) -> list[str]:
    errors: list[str] = []
    for term in case["required_terms"]:
        if term not in response:
            errors.append(f"缺少：{term}")
    for term in case["forbidden_terms"]:
        if term and term in response:
            errors.append(f"出现禁用词：{term}")
    if case["requires_labels"] and not any(label in response for label in LABELS):
        errors.append("缺少事实分层标签")
    if case["must_refuse"] and not any(word in response for word in REFUSAL_WORDS):
        errors.append("缺少明确拒绝")
    if case["strategy_contract"]:
        for term in STRATEGY_TERMS:
            if term not in response:
                errors.append(f"策略合同缺少：{term}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--responses", type=Path)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    try:
        cases = validate_cases(load_json(args.cases))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL  评测集：{error}")
        return 1

    categories = Counter(case["category"] for case in cases)
    print(f"PASS  评测集结构：{len(cases)}题，{len(categories)}类")
    print("      " + " · ".join(f"{name}:{count}" for name, count in sorted(categories.items())))

    if not args.responses:
        return 0

    try:
        responses = load_responses(args.responses)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL  回答文件：{error}")
        return 1

    case_by_id = {case["id"]: case for case in cases}
    unknown = sorted(set(responses) - set(case_by_id))
    if unknown:
        print(f"FAIL  未知回答id：{', '.join(unknown)}")
        return 1

    if not args.allow_partial and set(responses) != set(case_by_id):
        missing = sorted(set(case_by_id) - set(responses))
        print(f"FAIL  缺少{len(missing)}题回答；部分评分请加 --allow-partial")
        return 1

    failures = 0
    for case_id, response in responses.items():
        errors = score_response(case_by_id[case_id], response)
        if errors:
            failures += 1
            print(f"FAIL  {case_id}: {'；'.join(errors)}")
        else:
            print(f"PASS  {case_id}")

    total = len(responses)
    print(f"结果：{total - failures}/{total} 通过")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
