from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PlaygroundContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = (ROOT / "playground/index.html").read_text(encoding="utf-8")
        cls.js = (ROOT / "playground/app.js").read_text(encoding="utf-8")
        cls.core = (ROOT / "playground/core.js").read_text(encoding="utf-8")

    def test_accessible_controls_exist(self) -> None:
        for token in ('id="prompt"', 'aria-label="割味等级"', 'role="status"', 'id="generate"'):
            self.assertIn(token, self.html)

    def test_all_modes_are_interactive(self) -> None:
        for mode in range(5):
            self.assertIn(f'data-mode="{mode}"', self.html)

    def test_output_uses_text_content(self) -> None:
        self.assertIn("textContent", self.js)
        self.assertNotIn("innerHTML", self.js)

    def test_shared_core_owns_behavior(self) -> None:
        self.assertLess(self.html.index("./core.js"), self.html.index("./app.js"))
        self.assertIn("window.GeshenCore.createSession", self.js)
        self.assertNotIn("scenarioRules", self.js)
        self.assertIn("class GeshenSession", self.core)

    def test_offline_boundary_is_visible(self) -> None:
        self.assertIn("离线演示，不调用模型，不查询真实世界", self.html)


if __name__ == "__main__":
    unittest.main()
