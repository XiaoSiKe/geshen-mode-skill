from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.core = (ROOT / "references/core-models.md").read_text(encoding="utf-8")
        cls.case = (ROOT / "references/cases/jingtian-2026.md").read_text(encoding="utf-8")

    def test_entrypoint_is_progressively_disclosed(self) -> None:
        self.assertLessEqual(len(self.skill.splitlines()), 260)
        links = re.findall(r"\[[^\]]+\]\((references/[^)#]+)\)", self.skill)
        self.assertGreaterEqual(len(set(links)), 10)
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)

    def test_default_and_all_modes_exist(self) -> None:
        self.assertIn("默认：2级微割模式", self.skill)
        for phrase in ("0级退出", "1级正常", "2级微割", "3级全割", "4级割后复盘"):
            self.assertIn(phrase, self.skill)

    def test_fact_layers_and_hard_gate_exist(self) -> None:
        for marker in ("✅ 已确认", "🟡 单方说法", "🔵 框架推断", "🎭 戏仿生成"):
            self.assertIn(marker, self.skill)
        self.assertIn("当前无法核验", self.skill)
        self.assertIn("硬性交付门", self.skill)

    def test_models_and_heuristics_moved_to_owner(self) -> None:
        self.assertEqual(6, len(re.findall(r"^### 模型\d+：", self.core, re.M)))
        section = re.search(r"^## 10条决策启发式\n(.*?)(?=^## )", self.core, re.M | re.S)
        self.assertIsNotNone(section)
        self.assertEqual(10, len(re.findall(r"^\d+\. \*\*", section.group(1), re.M)))
        self.assertNotIn("### 模型1：", self.skill)

    def test_jingtian_case_keeps_procedural_boundary(self) -> None:
        self.assertIn("案件尚未进入实体审理", self.case)
        self.assertIn("不表示法院已经确认", self.case)
        self.assertIn("不代表和解、撤诉或结案", self.readme)

    def test_specific_asset_requests_cannot_bypass_refusal(self) -> None:
        self.assertIn("不承诺收益", self.skill)
        self.assertIn("拉盘方案", self.skill)
        self.assertIn("拒绝在段子之前", self.skill)

    def test_six_humor_packs_exist(self) -> None:
        files = list((ROOT / "references/humor").glob("*.md"))
        self.assertEqual(6, len(files))

    def test_source_ledger_is_structured(self) -> None:
        ledger = json.loads((ROOT / "references/source-ledger.json").read_text(encoding="utf-8"))
        self.assertEqual("2026-09-09", ledger["research_cutoff"])
        self.assertGreaterEqual(len(ledger["sources"]), 6)
        for source in ledger["sources"]:
            self.assertIn("does_not_prove", source)

    def test_user_requested_readme_line_stays_deleted(self) -> None:
        self.assertNotIn(
            "以上是本项目的戏仿文案，不是孙宇晨或 Claude 的原话。",
            self.readme,
        )
        self.assertFalse(self.readme.lstrip().startswith("!["))

    def test_version_is_consistent(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.3.0", version)
        for path in ("README.md", "SKILL.md", "CHANGELOG.md", "playground/index.html"):
            self.assertIn(version, (ROOT / path).read_text(encoding="utf-8"), path)

    def test_readme_has_humor_and_core(self) -> None:
        for phrase in (
            "三分割味，七分真东西",
            "AI申请退出群聊",
            "不是随机发疯",
            "6个核心模型",
        ):
            self.assertIn(phrase, self.readme)

    def test_ui_metadata_matches_skill(self) -> None:
        metadata = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "割神模式"', metadata)
        self.assertIn("$geshen-mode", metadata)


if __name__ == "__main__":
    unittest.main()
