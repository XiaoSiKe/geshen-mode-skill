from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_default_is_micro_mode(self) -> None:
        self.assertIn("默认：2级微割模式", self.skill)

    def test_all_modes_have_exit_or_recovery_path(self) -> None:
        for phrase in ("0级退出", "1级正常", "2级微割", "3级全割", "4级割后复盘"):
            self.assertIn(phrase, self.skill)

    def test_facts_inference_and_parody_are_distinguishable(self) -> None:
        for marker in ("✅ 已确认", "🟡 单方说法", "🔵 框架推断", "🎭 戏仿生成"):
            self.assertIn(marker, self.skill)

    def test_hard_delivery_gate_and_session_state_exist(self) -> None:
        self.assertIn("### Step 5：硬性交付门", self.skill)
        self.assertIn("当前无法核验", self.skill)
        self.assertIn("`current_mode`", self.skill)
        self.assertIn("`parody_notice_shown`", self.skill)
        self.assertIn("目标、三步动作、转化指标和止损线", self.skill)

    def test_jingtian_case_keeps_procedural_boundary(self) -> None:
        self.assertIn("案件尚未进入实体审理", self.readme)
        self.assertIn("法院最终裁判", self.skill)
        self.assertIn("不得把争议性陈述写成司法确认事实", self.skill)
        self.assertIn("即使用户要求站队", self.skill)

    def test_specific_asset_requests_cannot_bypass_refusal(self) -> None:
        self.assertIn("## 具体资产请求边界", self.skill)
        self.assertIn("不替用户给出个性化买卖指令", self.skill)
        self.assertIn("拒绝必须先于段子出现", self.skill)

    def test_skill_keeps_nuwa_model_count(self) -> None:
        models = re.findall(r"^### 模型\d+:", self.skill, re.M)
        self.assertGreaterEqual(len(models), 3)
        self.assertLessEqual(len(models), 7)

    def test_readme_explains_real_value_beyond_parody(self) -> None:
        self.assertIn("三分割味，七分真东西", self.readme)
        self.assertIn("注意力套利", self.readme)
        self.assertIn("割后复盘", self.readme)


if __name__ == "__main__":
    unittest.main()
