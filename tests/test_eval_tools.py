from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_eval_batch", ROOT / "scripts/build_eval_batch.py"
)
BUILD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BUILD)


class EvalToolTests(unittest.TestCase):
    def test_research_batch_contains_only_research_cases(self) -> None:
        cases = BUILD.select_cases(ROOT / "evals/cases.json", "research", None)
        self.assertEqual(4, len(cases))
        self.assertTrue(all(case["category"] == "research" for case in cases))

    def test_markdown_keeps_contract_separate(self) -> None:
        cases = BUILD.select_cases(ROOT / "evals/cases.json", "quality", 1)
        rendered = BUILD.render_markdown(cases)
        self.assertIn("提示：", rendered)
        self.assertIn("评测合同：", rendered)
        self.assertIn("不要把评测合同发送给答题模型", rendered)

    def test_jsonl_is_ready_for_captured_responses(self) -> None:
        cases = BUILD.select_cases(ROOT / "evals/cases.json", None, 2)
        rows = [json.loads(line) for line in BUILD.render_jsonl(cases).splitlines()]
        self.assertEqual(2, len(rows))
        self.assertTrue(all(row["response"] == "" for row in rows))

    def test_response_schema_requires_id_and_response(self) -> None:
        schema = json.loads(
            (ROOT / "evals/response-schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(["id", "response"], schema["required"])
        self.assertFalse(schema["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
