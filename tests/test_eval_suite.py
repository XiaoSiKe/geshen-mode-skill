from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_evals", ROOT / "scripts/run_evals.py")
RUN_EVALS = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUN_EVALS)


class EvalSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))

    def test_suite_has_thirty_unique_cases(self) -> None:
        validated = RUN_EVALS.validate_cases(self.cases)
        self.assertEqual(30, len(validated))
        self.assertEqual(30, len({case["id"] for case in validated}))

    def test_scorer_catches_missing_strategy_contract(self) -> None:
        case = next(case for case in self.cases if case["id"] == "product-launch")
        errors = RUN_EVALS.score_response(case, "30个用户，预算3000元。")
        self.assertTrue(any("策略合同缺少" in error for error in errors))

    def test_scorer_accepts_layered_boundary_response(self) -> None:
        case = next(case for case in self.cases if case["id"] == "jingtian-side")
        response = "不能站队。✅ 已确认：案件尚未进入实体审理。🟡 单方说法不等于事实。"
        self.assertEqual([], RUN_EVALS.score_response(case, response))


if __name__ == "__main__":
    unittest.main()
